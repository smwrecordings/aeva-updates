# plugin_handler.py

import os
import importlib.util
import traceback


class PluginHandler:
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = plugin_dir
        self.loaded_plugins = {}
        self._ensure_plugin_dir()

    def _ensure_plugin_dir(self):
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)
            print(f"📦 Plugin directory created: {self.plugin_dir}")

    def discover_plugins(self):
        return [f for f in os.listdir(self.plugin_dir) if f.endswith(".py")]

    def load_plugin(self, plugin_name):
        path = os.path.join(self.plugin_dir, plugin_name)
        if not os.path.exists(path):
            return f"❌ Plugin '{plugin_name}' not found."

        try:
            spec = importlib.util.spec_from_file_location(plugin_name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.loaded_plugins[plugin_name] = module
            return f"✅ Plugin '{plugin_name}' loaded."
        except Exception as e:
            return f"❌ Failed to load {plugin_name}: {e}"

    def execute_plugin(self, plugin_name, *args, **kwargs):
        if plugin_name not in self.loaded_plugins:
            load_result = self.load_plugin(plugin_name)
            print(load_result)
            if "❌" in load_result:
                return load_result

        try:
            plugin = self.loaded_plugins[plugin_name]
            if hasattr(plugin, "run"):
                return plugin.run(*args, **kwargs)
            else:
                return f"⚠️ Plugin '{plugin_name}' has no 'run()' method."
        except Exception as e:
            traceback.print_exc()
            return f"❌ Error running '{plugin_name}': {str(e)}"
