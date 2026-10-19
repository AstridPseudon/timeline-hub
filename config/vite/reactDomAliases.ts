import path from "path";

/** Keep React DOM package resolution intact while routing its client server subpath to the browser renderer. */
export const createReactDomAliases = (nodeModulesRoot: string) => ({
  "react-dom/server": path.resolve(nodeModulesRoot, "react-dom/server.browser.js"),
  "react-dom": path.resolve(nodeModulesRoot, "react-dom"),
});
