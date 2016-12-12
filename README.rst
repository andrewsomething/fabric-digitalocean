===================
fabric-digitalocean
===================

.. image:: https://travis-ci.org/andrewsomething/fabric-digitalocean.svg?branch=master
    :target: https://travis-ci.org/andrewsomething/fabric-digitalocean

fabric-digitalocean is a collection of tools aiming to make it easy to use
`Fabric`_ and `DigitalOcean`_ together.

It was inspired by `fabric-aws`_

Installation
------------

```
pip install fabric-digitalocean
```

Usage
-----

With fabric-digitalocean, you can decorate Fabric tasks to run on a set of
DigitalOcean Droplet. The `@droplets` decorator can take a list of Droplet IDs,
a tag, or a region as an argument. If you use a tag or region, it will be
expanded to a list of all Droplets with that tag applied or in that region.
They can also be used together.

The environmental variable `FABRIC_DIGITALOCEAN_TOKEN` must contain a
DigitalOcean API token.

See below for an example:

.. code-block:: python

    from fabric.api import task, run
    from fabric_digitalocean.decorators import droplets


    @task
    @droplets(ids=[8043964, 7997777])
    def task_by_ids():
        run('hostname')
        run('uptime')


    @task
    @droplets(tag='demo')
    def task_by_tag():
        run('hostname')
        run('uptime')


    @task
    @droplets(region='nyc3')
    def task_by_region():
        run('hostname')
        run('uptime')


    @task
    @droplets(region='nyc2', tag='demo')
    def task_by_both():
        run('hostname')
        run('uptime')


Testing
-------

To run the test suite, use:

.. code-block::
    nosetests -v --with-coverage --cover-package=fabric_digitalocean


.. _Fabric: http://www.fabfile.org/
.. _DigitalOcean: https://www.digitalocean.com
.. _fabric-aws: https://github.com/EverythingMe/fabric-aws
