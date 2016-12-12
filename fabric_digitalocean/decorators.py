import digitalocean
import os

from fabric.decorators import wraps, _wrap_as_new


class TokenError(Exception):
    pass


def _list_annotating_decorator(attribute, *values):
    """
    From fabric.decorators._list_annotating_decorator
    https://github.com/fabric/fabric/blob/master/fabric/decorators.py#L49
    """
    def attach_list(func):
        @wraps(func)
        def inner_decorator(*args, **kwargs):
            return func(*args, **kwargs)
        _values = values
        # Allow for single iterable argument as well as *args
        if len(_values) == 1 and not isinstance(_values[0], basestring):
            _values = _values[0]
        setattr(inner_decorator, attribute, list(_values))
        # Don't replace @task new-style task objects with inner_decorator by
        # itself -- wrap in a new Task object first.
        inner_decorator = _wrap_as_new(func, inner_decorator)
        return inner_decorator
    return attach_list


def droplet_generator(region=None, tag=None, ids=[]):
    """
    A generator that yields Droplet IP addresses.

    :param region: A DigitalOcean region
    :type region: str

    :param tag: A DigitalOcean tag name
    :type tag: str

    :param id: A list of DigitalOcean Droplet IDs
    :type id: list
    """
    token = os.getenv('FABRIC_DIGITALOCEAN_TOKEN')
    if not token:
        raise TokenError('The environmental variable FABRIC_DIGITALOCEAN_TOKEN'
                         ' is empty. It must contain a valid DigitalOcean API'
                         ' token.')

    client = digitalocean.Manager(token=token)
    hosts = []

    if not ids:
        droplets = client.get_all_droplets(tag_name=tag)
        for d in droplets:
            if not region or d.region['slug'] == region:
                hosts.append(d)
    else:
        if isinstance(ids, int):
            droplet = client.get_droplet(droplet_id=ids)
            hosts.append(droplet)
        else:
            for i in ids:
                droplet = client.get_droplet(droplet_id=i)
                hosts.append(droplet)

    for h in hosts:
        yield h.ip_address


@wraps(droplet_generator)
def droplets(region=None, tag=None, ids=[]):
    """
    Fabric decorator for running a task on DigitalOcean Droplets.

    :param region: A DigitalOcean region
    :type region: str

    :param tag: A DigitalOcean tag name
    :type tag: str

    :param id: A list of DigitalOcean Droplet IDs
    :type id: list
    """
    return _list_annotating_decorator('hosts',
                                      droplet_generator(region,
                                                        tag,
                                                        ids))
