## ERD

![d229fbdc10bf1c6134841b37caf0d094](https://github.com/niallc18/events_api/assets/109161441/fc08cde4-8ee8-41f4-8965-8b0fdb8f5d1d)

## Usage Instructions

- Make sure you have Python installed, I used 3.9 in a conda environment.
- Clone repo and navigate to the events_api directory.
- Run pip install for following:

```shell

pip install fastapi[all] sqlalchemy
pip install pytest pytest-asyncio

```

- Run unit tests:

```shell

pytest test_main.py

```

For manual testing using Postman, run the population script:

```shell

python3 populate.py

```

Then open a seperate terminal and navigate to the events_api directory and start the app:

```shell

uvicorn main:app --reload

```

You should now be able to test the routes using Postman, refer to the following video for a brief tutorial: https://www.loom.com/share/2be06c6955dd4fc5a0f8e8f84a0e287d?sid=e46f3af2-70cd-469f-bbc0-a3a4d7c8d99f

You can also check out the Swagger UI when running the app, enter the following into your browser: http://127.0.0.1:8000/docs

## References

- https://devdocs.io/fastapi/
- https://www.youtube.com/watch?v=nC9ob8xM3AM
- https://stackoverflow.com/questions/78126386/how-to-extend-a-pytest-base-class-and-override-a-fixture
