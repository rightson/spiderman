# spiderman

This is a data-driven selenium wrapper.

This tool can help you navigate the web browser by simply defining a series of steps without writing the code.

## Define the steps

First, you should create a JSON file and define desired steps in an array.
Each step should be contain an `action` and its corresponding action data.
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
        },
        {
            "action": "pause"
        }
    ]
}

```

Available actions and corresponding action data are listed as below:
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
- `pause`

If you need more actions, feel free to let me know or just extend it (PR is welcome). Thanks!

## Run the code

```
python spiderman.py steps.json
```

Enjoy : )