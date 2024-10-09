# GMU Daily Permit Automation

Selenium Script to speed up the manual process of purchasing
Daily (Parking) Permit from https://gmu.t2hosted.com/per/selectpermit.aspx.

Use the Script to purchase following supported Permit:
* `Evening General Permit (only valid from 4:00pm-11:59pm)`

> [!IMPORTANT]
> 2FA [with Duo](https://duo.com/) is still necessary. 
> Please keep your phone handy when running the Script.

## Quickstart

> [!CAUTION]
> Remember to double check and set [parking date](./config.template.toml#L8) each script run!
> Find this under the `[parking]` section in `config.toml`.

1. Clone this repo into your local machine.

    ```sh
    git clone https://github.com/rnag/GMU-Daily-Permit-Automation.git
    cd GMU-Daily-Permit-Automation
    ```

2. Fill out [`config.template.toml`](./config.template.toml), and rename to `config.toml`.
3. Download [Python](https://www.python.org/downloads/) if needed, and [set up a virtual environment](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/). Activate `venv`.
4. Install project dependencies with `pip` (*Script requires Python 3.8+*)
    ```shell
   (.venv) ➜  GMU-Daily-Permit-Automation git:(main) $ pip install -r requirements.txt   
    ```
5. Run the Script

   ```shell
   python main.py
   ```

## Motivation (or Rationale)

As a current, part-time graduate student @ [George Mason](https://www.gmu.edu/), I usually take 1 class per semester,
and it's more cost-effective to purchase the Daily Permit, as opposed to a Weekly or Semester Permit.

However, purchasing a Daily Permit is a time-consuming process, and I usually procrastinate and leave it off till
the last minute (day of) which results in added stress on my part.

This Script aims to solve my longstanding issue, and enable me to more easily
purchase Daily Permit for the date of class.

