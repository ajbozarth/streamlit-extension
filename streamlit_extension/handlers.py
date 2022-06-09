import json

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
from streamlit_extension.process_manager import StreamlitManager
import tornado


class RouteHandler(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        self.finish(json.dumps({
            "data": "This is /streamlit/test endpoint!"
        }))

    @tornado.web.authenticated
    def post(self):
        # parse filename and location
        json_payload = self.get_json_body()
        streamlit_app_filepath = json_payload['file']

        port = StreamlitManager.instance().start(streamlit_app_filepath=streamlit_app_filepath)

        self.finish(json.dumps({
            "data": "This is /streamlit/test endpoint!",
            "url": f"http://localhost:{port}"
        }))

    @tornado.web.authenticated
    def delete(self):
        # parse filename and location
        json_payload = self.get_json_body()
        streamlit_app_filepath = json_payload['file']

        StreamlitManager.instance().stop(streamlit_app_filepath=streamlit_app_filepath)


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "streamlit", "test")
    handlers = [(route_pattern, RouteHandler)]
    web_app.add_handlers(host_pattern, handlers)
