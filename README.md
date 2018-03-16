# Overview
Install, configure and manage the AWS scicomp account.


## Instructions to create or update CF stacks

```
# unlock repo
git-crypt unlock
# set env vars
source env_vars && source env_vars.secret
# Run commands in update_cf_stack.sh to update CF stacks
```

The above should setup resources for the account.  Once the infrastructure for the account has been setup
you can access and view the account using the [AWS console](https://AWS-account-ID-or-alias.signin.aws.amazon.com/console).

*Note - This project depends on CF templates from other accounts.*

## Scicomp


## Continuous Integration
We have configured Travis to deploy CF template updates.  Travis does this by running update_cf_stack.sh on every
change.


# Contributions

## Issues
* https://sagebionetworks.jira.com/projects/IT

## Builds
* https://travis-ci.org/Sage-Bionetworks/scicomp-infra

## Secrets
* We use [git-crypt](https://github.com/AGWA/git-crypt) to hide secrets.
Access to secrets is tightly controlled.  You will be required to
have your own [GPG key](https://help.github.com/articles/generating-a-new-gpg-key)
and you must request access by a maintainer of this project.
