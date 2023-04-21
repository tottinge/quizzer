# Quizzology

It runs.

Monitoring (we need a unified dashboard or tool): 
* [Github](https://github.com/tottinge/quizzer/actions )
* [Heroku](https://dashboard.heroku.com/apps/quizzology/activity)

We periodically have to update the [ChromeDriver](https://chromedriver.chromium.org/downloads).
* Download the chrome driver to the webdrivers/_os_/ directory.
* Delete the old `chromedriver` file
* unzip the new chromedriver zip file
* right-click on the chromedriver and open it
* give permission to run the chrome driver
* run the ui-tests


Currently, Quizzology is a slow-coding target. We work on it a bit at a time, and constantly refer to the
charter except when there is some shiny idea we want to chase.

We started pretty much architecture and design free. 

The purpose of this project is not so much to make a project, but to intentionally and carefully practice TDD,
refactoring, evolutionary design, and minimalism.

Don't look at it as a finished product, but a starting point for doing fun stuff.
* We've added W3.CSS and some HTML5, probably more than we originally intended.
* We made a heroku app out of this, with GitHub actions for CI
* We started using type hints to enable better IDE support.
* We've added TinyDB and are transitioning to MongoDB in short order
* We got interested in selenium and wrote selenium tests of some basic features.
* We also got interested in BDD and wrote some Behave tests using the model object 
(at the time 'quizzology' class) so that Gherkin was an alternative UI.
* We dug a bit into Bottle (web framework) lore and found webtest, and will likely move
  our web wiring tests into webtest because it's so much faster than standing up a web server,
  and is still basic wsgi operation.

In the works:
* Create some kind of identity so our results and other people's results aren't all mixed together
* Remember past sessions, so we can re-quiz on quizzes and questions from past
* Keep track of questions that we've missed most, and refresh on those
* Make it look less awful


Chrome drivers are available at https://chromedriver.chromium.org/downloads 

# Initial Setup for Local Mongodb

## Install docker and launch it. 
`brew install docker`

You will need to launch this and give the Mac permission to run it.

## Install a Front-end for Mongo

`brew install mongodb-compass`

This gets us the UI for doing data stuff in mongo.

Again, you'll need to launch it and give the Mac permission to run it.

## Download mongo and run it as 'quizzology-data'

`docker run -p 27017:27017 --name quizzology-data -d -e MONGO_INITDB_ROOT_USERNAME=root -e MONGO_INITDB_ROOT_PASSWORD=passme mongo
`

The image should be running in the background (you get a hash code for 
it), and should appear in your docker desktop dashboard.

## Install the login table


