import esbuild from "esbuild";

const isWatch = process.argv.includes("--watch");

const config = {
  entryPoints: ["src/index.js"],
  bundle: true,
  outfile: "dist/contentScript.js",
  format: "iife",
  platform: "browser",
  sourcemap: true
};

if (isWatch) {
  const ctx = await esbuild.context(config);
  await ctx.watch();
  console.log("Watching for changes...");
} else {
  await esbuild.build(config);
  console.log("Build complete");
}
