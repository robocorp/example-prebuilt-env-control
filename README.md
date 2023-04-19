# Robot implementations for running and managing prebuilt environments with RCC

The robots here enable you to pre-built RCC environments on normal Workers via Control Room process:

## Builder

Robot for creating pre-built environments:
* Environment config given in workitem
* Built the environment using RCC
* Example shows pushing to S3, but you can replace this with basically any file server / service


## Importer
Robot the "publishes" pre-built environments to RCC Remote.
This robot is meant to be executed on the machine that is running rcc-remote service.

* Download the pre-built environment from S3
  * You can replace the S3 with file service of your choosing
* Imports the pre-built environment so that rcc-remote service is able to distribute the environment to tools and users.

> Note that here you can inject process tools and steps of yous choosing:
Manual approvals, virus scanners, etc.

For more details checkout our [docs on the topic](https://robocorp.com/docs/rcc/pre-built-environments)