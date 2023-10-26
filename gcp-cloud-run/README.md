# Instructions for getting up and running in GCP Cloud Run

Reference https://cloud.google.com/code/docs/vscode/deploy-cloud-run-app

## Prereq
1. Install and setup the Google Cloud CLI
2. Add the Google Cloud Code extension to VSCode
2. Sign in to Cloud Code. Click on CLoud Code allong the bottom of VSCode and it will launch GCP
3. Select a project. You can click on the same Cloud Code icon which will launch the command pallet and you can select a project

## {Optional} Local build testing
You can test your docker buildfile locally by using docker desktop.
If you have the docker extension to VSCode you can right click a Dockerfile to build the image.
It is also possible to use the Cloud Code extrension to do local Cloud Run testing which uses Minikube under the covers.

## Deploy
1. Open the Command Palette (press Ctrl/Cmd+Shift+P
2. Run the Deploy to Cloud Run command
3. Select to use your existing CLI and update if nessesary
4. Choose a name for the servce and select the region and "Cloud Build"
5. Click Deploy 
5. Cloud Code builds your image, pushes it to the registry, and deploys your service to Cloud Run.
6. To view your running service, open the URL displayed at the top of the Deploy to Cloud Run dialog.
