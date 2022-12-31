# spiderman

This is a data-driven selenium wrapper.

You can simply control the browser by defining the flow file.

## Define the flow file

Create a flow file and define desired steps.
Each step should be composed of an `action` and some action data.
For example:

```json
{
    "steps": [
        {
            "action": "get",
            "url": "https://www.google.com/"
        },
        {
            "action": "send_keys",
            "xpath": "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input",
            "key": "https://github.com/rightson/"
        },
        {
            "action": "click",
            "xpath": "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[4]/center/input[1]"
        }
    ]
}

```

Available actions and action data are:
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