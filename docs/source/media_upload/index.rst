.. _Media Upload:

Media Upload
============

.. image:: ./images/media_upload.png

Piccolo Admin has the option of uploading media files to local static folder 
(local storage). Multi file upload is enabled per record for all columns 
specified in ``media_columns``. 


Usage
-----

Piccolo admin uses the Piccolo ORM `Array <https://piccolo-orm.readthedocs.io/en/latest/piccolo/schema/column_types.html#array>`_ 
column for media uploads. You must specify the column in the table and then register 
the media column in the ``TableConfig`` ``media_columns``  
so that the admin UI can display the file upload box for that field by
inspecting the JSON schema. The final step is to write your own media handler that 
upload the files and register handler to ``TableConfig`` ``media_handler``.

Full example:

.. code-block:: python

    import shutil
    import typing as t
    import uuid
    from dataclasses import dataclass
    from piccolo.columns import Array, Varchar
    from piccolo_admin.endpoints import  (
        MEDIA_PATH, 
        TableConfig, 
        create_admin
    )

    class Movie(Table):
        poster = Array(base_column=Varchar())


    @dataclass
    class LocalMediaHandler:
        root_path: str

        # This is an example of a upload method, but you can write your own
        # to suit your needs. The method must have request and file arguments.
        def upload(self, request, file):
            image = f"{self.root_path}/{uuid.uuid4()}.jpeg"
            image_path = "/".join(image.split("/")[-2:])
            with open(image, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            url_path = dict(request.scope["headers"]).get(b"host", b"").decode()
            return {"image": f"{request.url.scheme}://{url_path}/{image_path}"}


    media_handler: t.Any = LocalMediaHandler(root_path=MEDIA_PATH)

    movie_config = TableConfig(
        table_class=Movie,
        media_columns=[Movie.poster],
        media_handler=media_handler,
    )

    APP = create_admin([movie_config])

