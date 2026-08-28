import glob

class PluginBundlerPlugin:
    def __init__(self, target_pattern="*_plugin.py", output_file="bundle_core.py"):
        self.target_pattern = target_pattern
        self.output_file = output_file
        print("-> 📦 [打包重構外掛] 模組合併工具初始化成功！")

    def bundle_plugins(self):
        """將多個外掛檔案合併打包成單一核心檔案"""
        plugin_files = glob.glob(self.target_pattern)
        print(f"-> 🔍 正在打包 {len(plugin_files)} 個外掛模組...")

        with open(self.output_file, 'w', encoding='utf-8') as outfile:
            outfile.write("# === Auto-Generated Bundled Core System ===\n")
            for filepath in sorted(plugin_files):
                if filepath == self.output_file:
                    continue
                outfile.write(f"\n# --- Source: {filepath} ---\n")
                with open(filepath, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                outfile.write("\n")

        print(f"-> ✅ 打包完成！所有模組已成功合併至: {self.output_file}")

if __name__ == "__main__":
    bundler = PluginBundlerPlugin()
    bundler.bundle_plugins()
