===================
fabric-digitalocean
===================

fabric-digitalocean is a collection of tools aiming to make it easy to use
`Fabric`_ and `DigitalOcean`_ together.

It was inspired by `fabric-aws`_

Examples
--------
::

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


.. _Fabric: http://www.fabfile.org/
.. _DigitalOcean: https://www.digitalocean.com
.. _fabric-aws: https://github.com/EverythingMe/fabric-aws
