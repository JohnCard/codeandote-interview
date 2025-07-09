## Country model documentation

**List every Country instances**

-   **Endpoint:** `/consuming_api/countries`
-   **Method:** `GET`
-   **Description:** Getting all data from Country model database by json formats.
-   **Response body:**

```json
{
    "count": 250,
    "next": "http://127.0.0.1:8000/consuming_api/countries?page=2",
    "previous": null,
    "results": [
        {
            "id": 231,
            "name": "Dominican Republic",
            "region": "Americas",
            "subregion": "Caribbean",
            "capital": "Santo Domingo",
            "population": 10847904,
            "latitude": 19,
            "longitude": -70,
            "area": 48671.0,
            "flag": "The flag of the Dominican Republic is divided into four rectangles by a centered white cross that extends to the edges of the field and bears the national coat of arms in its center. The upper hoist-side and lower fly-side rectangles are blue and the lower hoist-side and upper fly-side rectangles are red."
        },
        {
            "id": 232,
            "name": "Guyana",
            "region": "Americas",
            "subregion": "South America",
            "capital": "Georgetown",
            "population": 786559,
            "latitude": 5,
            "longitude": -59,
            "area": 214969.0,
            "flag": "The flag of Guyana has a green field with two isosceles triangles which share a common base on the hoist end. The smaller black-edged red triangle spanning half the width of the field is superimposed on the larger white-edged yellow triangle which spans the full width of the field."
        },
        .....
    ]
}
```

**Create new Country instances**

-   **Endpoint:** `/consuming_api/countries`
-   **Method:** `POST`
-   **Description:** Creates a new Country instance.
-   **Request body:**

```json
{
    "name": "Dominican Republic",
    "region": "Americas",
    "subregion": "Caribbean",
    "capital": "Santo Domingo",
    "population": 10847904,
    "latitude": 19,
    "longitude": -70,
    "area": 48671.0,
    "flag": "The flag of the Dominican Republic is divided into four rectangles by a centered white cross that extends to the edges of the field and bears the national coat of arms in its center. The upper hoist-side and lower fly-side rectangles are blue and the lower hoist-side and upper fly-side rectangles are red."
}
```

**Retrieve one Country**

-   **Endpoint:** `/consuming_api/countries/<int:id>`
-   **Method:** `GET`
-   **Description:** Gets one specific Country by it´s id.
-   **Response body:**

```json
{
    "id": 481,
    "name": "Dominican Republic",
    "region": "Americas",
    "subregion": "Caribbean",
    "capital": "Santo Domingo",
    "population": 10847904,
    "latitude": 19,
    "longitude": -70,
    "area": 48671.0,
    "flag": "The flag of the Dominican Republic is divided into four rectangles by a centered white cross that extends to the edges of the field and bears the national coat of arms in its center. The upper hoist-side and lower fly-side rectangles are blue and the lower hoist-side and upper fly-side rectangles are red."
}
```

**Update one specific Country**

-   **Endpoint:** `/consuming_api/countries/<int:id>`
-   **Method:** `PUT`
-   **Description:** Updates one specific patient by it´s id.
-   **Resquest body:**

```json
{
    "name": "Dominican Republic",
    "region": "Americas updated",
    "subregion": "Caribbean updated",
    "capital": "Santo Domingo",
    "population": 34290843,
    "latitude": 25,
    "longitude": -80,
    "area": 48674.0,
    "flag": "Flag description updated test."
}
```

**Delete one specific Country**

-   **Endpoint:** `/consuming_api/countries/<int:id>`
-   **Method:** `DELETE`
-   **Description:** Deletes one specific patient by it´s id.
-   **Response body:**

```
Empty data response
```

**Delete one specific Country**

-   **Endpoint:** `/consuming_api/countries/<int:id>`
-   **Method:** `DELETE`
-   **Description:** Deletes one specific patient by it´s id.
-   **Response body:**

```
Empty data response
```

**Create new Country instances**

-   **Endpoint:** `/consuming_api/generic`
-   **Method:** `POST`
-   **Description:** Creates a new Country instance based on a name payload/parameter.
-   **Request body:**

```json
{
    "country_name": "mexico"
}
```

-   **Response body:**

```json
{
    "ok": true,
    "succes": "New country created"
}
```

**New countries using masive data**

-   **Endpoint:** `/consuming_api/generic`
-   **Method:** `PUT`
-   **Description:** Updates masive data to create new Country instances based on a limit & init parameters.
-   **Resquest body:**

```json
{
    "limit": 500,
    "init": 1
}
```

-   **Response body:**

```json
{
    "ok": true,
    "succes": "Countries created"
}
```


**Return excel report summary**

-   **Endpoint:** `/consuming_api/excel_report`
-   **Method:** `GET`
-   **Description:** Returns a complete excel report/summary with graphs & tables analyzing main countries data.
-   **Response body:**

```json
{
	"file": "<file_data>"
}
```