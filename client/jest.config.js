module.exports = {
    preset: '@vue/cli-plugin-unit-jest',
    verbose: true,
    moduleFileExtensions: [
        'js',
        'json',
        'vue'
    ],
    collectCoverage: true,
    coverageDirectory: './tests/coverage',
    collectCoverageFrom: ['src/components/*.{js,vue}', 'src/views/*.{js,vue}', '!/node_modules/'],
    coverageReporters: ['text-summary']
}
