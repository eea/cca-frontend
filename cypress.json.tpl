{
  "baseUrl": "http://localhost:3000",
  "viewportWidth": 1280,
  "defaultCommandTimeout": 8888,
  "chromeWebSecurity": false,
  "reporter": "junit",
  "video": true,
  "retries": {
    "runMode": 8,
    "openMode": 0
  },
  "reporterOptions": {
    "mochaFile": "cypress/reports/cypress-[hash].xml",
    "jenkinsMode": true,
    "toConsole": true
  },
  "integrationFolder": "src/addons",
  "testFiles": "**/cypress/integration/**/*.js",
  "fixturesFolder": "./src/addons/volto-slate-zotero/cypress/fixtures",
  "videoUploadOnPasses": false,
  "screenshotOnRunFailure": false
}
