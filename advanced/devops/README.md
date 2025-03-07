# CI/CD 

## Workflows 

### deploy-clever-cloud
The [workflow](./deploy-clever-cloud.yaml) will be triggered for each new commit pushed on main branch. It's composed of three steps : 
* Tag generation based on **app-name** input, e.g app-name=frontend, then the tag will be : frontend.0.0.<nbOfCommits> since the first tag of this kind. 
* Release creation, create a release based on the generated tag. 
* Clever cloud deployment, it push to a clever cloud repository main branch, identified by the input **app-id**

You can find an example [here](https://github.com/dataforgoodfr/13_brigade_coupes_rases/blob/main/.github/workflows/frontend-ci.yml) 