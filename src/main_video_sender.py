import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GLib
from messaging import zmq_sub, send_json, recv_json
import threading

Gst.init(None)

# Two analysis machines — they listen on ports 6001 and 6002
FACE_ANALYZER_IP = "192.168.1.20"
LPR_ANALYZER_IP  = "192.168.1.30"

# They send back results on these ports:
RESULT_PORT_FACE = 7001
RESULT_PORT_LPR  = 7002

blacklist_faces = {"john_doe", "mark_smith"}
blacklist_plates = {"ABC1234", "XYZ9876"}

def receive_results(face_cb, lpr_cb):
    """Thread: receives results from both analyzers."""
    face_sock = zmq_sub(FACE_ANALYZER_IP, RESULT_PORT_FACE)
    lpr_sock  = zmq_sub(LPR_ANALYZER_IP, RESULT_PORT_LPR)

    while True:
        result_face = recv_json(face_sock)
        face_cb(result_face)

        result_lpr = recv_json(lpr_sock)
        lpr_cb(result_lpr)


def on_face_result(data):
    name = data.get("name")
    if name in blacklist_faces:
        print(f"⚠️ BLACKLISTED FACE DETECTED: {name}")

def on_lpr_result(data):
    plate = data.get("plate")
    if plate in blacklist_plates:
        print(f"🚨 BLACKLISTED LICENSE PLATE: {plate}")


def main():
    # Launch receiving thread
    threading.Thread(target=receive_results,
                     args=(on_face_result, on_lpr_result),
                     daemon=True).start()

    # GStreamer pipeline: capture webcam and send RTP stream
    pipeline_str = """
        v4l2src !
        videoconvert !
        x264enc tune=zerolatency bitrate=800 speed-preset=superfast !
        rtph264pay config-interval=1 pt=96 !

        tee name=t

        t. ! queue ! udpsink host={FACE} port=5001
        t. ! queue ! udpsink host={LPR} port=5002
    """.format(FACE=FACE_ANALYZER_IP, LPR=LPR_ANALYZER_IP)

    pipeline = Gst.parse_launch(pipeline_str)
    pipeline.set_state(Gst.State.PLAYING)

    print("Sending video stream...")
    loop = GLib.MainLoop()
    loop.run()


if __name__ == "__main__":
    main()
