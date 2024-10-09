# GMU Daily Permit Automation

Selenium Script to speed up the manual process of purchasing
Daily (Parking) Permit from https://gmu.t2hosted.com/per/selectpermit.aspx.

Use the Script to purchase following supported Permit:
* `Evening General Permit (only valid from 4:00pm-11:59pm)`

> [!IMPORTANT]
> 2FA [with Duo](https://duo.com/) is still necessary. 
> Please keep your phone handy when running the Script.

## Quickstart

1. Clone this repo into your local machine.

    ```sh
    git clone https://github.com/rnag/GMU-Daily-Permit-Automation.git
    ```

2. Fill out [`config.template.toml`](./config.template.toml), and rename to `config.toml`.
3. Download [Python](https://www.python.org/downloads/) if needed, and [set up a virtual environment](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/). Activate `venv`.
4. Install project dependencies with `pip install` (*Requires Python 3.8+*)
    ```shell
   (.venv) ➜  GMU-Daily-Permit-Automation git:(main) $ pip install -r requirements.txt   
    ```
5. Run the Script

   > [!CAUTION] Remember to double check and set [parking date](./config.template.toml#L8) each script run! Find this under the `[parking]` section in `config.toml`.
 
    ```shell
    python main.py
    ```
