# Coding Challenge

This Code assessment represents a coding challenge for Engineering roles.

## Purpose

- Evaluate your coding abilities and your software engineering skills
- Judge your technical experience
- Understand how you break down existing code bases and problem solve
- Have a technical conversation after the code submission & review is done

## Submission

First steps
1. Use your own Github account to clone this repository.
 
Once the activity is completed:
1. Commit/ push your code into your own Git. 
2. DONT try to raise a Pull Request to this repo please.
3. Make your GitHub repo as private. (GitHub -> Settings -> General -> Danger Zone -> Change repository visibility -> Change Visibility -> Make Private)
4. Share the access projectforyou20@gmail.com (GitHub -> Settings -> Collaborators -> Manage Access -> Add People -> Add the email address projectforyou20@gmail.com)
5. Share the GitHub repository URL with hiring team.

We will review your work and get back to you!


# Introduction
An old and unfinished piece of work needs to be revived. 

This old repository was intended to produce a scalable flask api for reading and writing to a "wallet"

We would like to return the code/services here to a runnable state in stages. 

## Stage 1: Base code and tests

Read over the small codebase present in ./src

A convenience virtualenv bootstrap script is present in 'virtual.sh' begin by `source virtual.sh`

The stage is complete when:
- [ ] Makefile stage 'unit_test_python' executed by `make unit_test_python` passes


## Stage 2: Dockerised code
A poorly configured/outdated dockerfile is intended to build the app, please restore/optimise it. 

The stage is completed when:
- [ ] Makefile stage 'unit_test_docker' passes, executed by `make unit_test_docker`


## Stage 3a: docker-compose services
The supporting services for serving the wallet api are present in docker-compose.traefik.yml. 

Code present in the `labels` section has already been verified to work by the testing team. 

The stage is completed when:

- [ ] 'make up_traefik' shows urls protected by basic auth
    - [ ] https://traefik.localhost/dashboard/
    - [ ] https://prometheus.localhost/
    - [ ] https://whoami.localhost/
- [ ] Test that you can access the whoami with curl.


## Stage 3b: docker-compose api
The wallet API is served in the file 'docker-compose.yml' 

Correct this file and any others to ensure the wallet API status operates. 

The stage is completed when:

- [ ] the Makefile stage 'up' provides the following functionality:
    - [ ] docker healthchecks show healthy
    - [ ] wallet api service can be seen in the traefik dashboard 
    - [ ] wallet status is visible via https://wallet.localhost/status
    - [ ] calling the wallet status can be in prometheus

## Stage 4: Wallet (Extension)

- [ ] Create API endpoints for adding funds
- [ ] Create API endpoints for removing funds
- [ ] Externalise the balance to create a threadsafe wallet

### Contact
* For any questions, please contact the hiring person/team who contacted you.

