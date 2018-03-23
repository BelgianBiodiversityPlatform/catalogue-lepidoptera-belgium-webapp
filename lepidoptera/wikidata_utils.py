from wikidata.client import Client


def get_images_for_entity(q_identifier):
    # Returns a list of <wikidata.commonsmedia.File>
    client = Client()
    entity = client.get(q_identifier, load=True)
    image_prop = client.get('P18')
    return entity.getlist(image_prop)


def get_images_url_for_entity(q_identifier):
    return [image.image_url for image in get_images_for_entity(q_identifier)]