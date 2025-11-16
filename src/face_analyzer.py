import gi
gi.require_version("Gst", "1.0")
from gi.repository import Gst, GLib
from messaging import zmq_pub, send_json
import random
import threading

Gst.init(None)
RESULT_PORT = 7001
result_sock = zmq_pub(RESULT_PORT)

# Dummy face recognition function
def recognize_face(frame):
    names = ["unknown", "john_doe", "mary", "mark_smith"]
    return random.choice(names)

def gst_new_sample(sink):
    sample = sink.emit("pull-sample")
    buffer = sample.get_buffer()

    # Fake recognition:
    name = recognize_face(buffer)

    send_json(result_sock, {"name": name})
    return Gst.FlowReturn.OK

def main():
    pipeline_str = """
        udpsrc port=5001 caps="application/x-rtp,encoding-name=H264,payload=96" !
        rtph264depay ! avdec_h264 !
        videoconvert !
        appsink name=framesync emit-signals=true sync=false max-buffers=1 drop=true
    """

    pipeline = Gst.parse_launch(pipeline_str)
    sink = pipeline.get_by_name("framesync")
    sink.connect("new-sample", gst_new_sample)

    pipeline.set_state(Gst.State.PLAYING)
    print("Face analyzer running...")
    GLib.MainLoop().run()

if __name__ == "__main__":
    main()
