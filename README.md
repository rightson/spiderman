# spiderman

This is a simple selenium wrapper.

You can simply control the browser by defining the flow file.

## Define the flow

Create a flow (JSON) and defines steps:

```json
{
    "steps": [
        {
            "action": "get",
            "url": "https://www.google.com/"
        }
    ]
}

```

Each step should contain an `action` and its corresponding arguments.

Available actions/arguments are:
- `get`
  - url
- `select`
  - xpath
  - text
- `click`
  - xpath
- `window`
  - index
- `ocr`
  - img_xpath
  - regen_xpath
  - input_xpath
- `send_keys`
  - xpath
  - key

## Run the code

```
python spiderman.py your_flow.json
```

Enjoy : )