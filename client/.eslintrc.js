module.exports = {
	root: true,
	env: {
		node: true,
	},
	extends: ["plugin:vue/vue3-essential", "eslint:recommended"],
	parserOptions: {
		parser: "@babel/eslint-parser",
	},
	parserOptions: {
		sourceType: "module",
		babelOptions: {
			configFile: path.join(__dirname, "babel.config.js"),
		},
	},
	rules: {
		"no-console": process.env.NODE_ENV === "production" ? "warn" : "off",
		"no-debugger": process.env.NODE_ENV === "production" ? "warn" : "off",
		"vue/script-indent": ["error", 2, { baseIndent: 1 }],
	},
	overrides: [
		{
			files: [
				"**/__tests__/*.{j,t}s?(x)",
				"**/tests/unit/**/*.spec.{j,t}s?(x)",
			],
			env: {
				jest: true,
			},
		},
	],
};
