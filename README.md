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
> Remember to double check and set [parking date](#parking-date) each script run!

1. Download [Python](https://www.python.org/downloads/) if needed.
2. Install this project with `pip`. Requires Python 3.8+.
    ```sh
    pip install git+https://github.com/rnag/GMU-Daily-Permit-Automation.git
    ```
3. Run `gmu c` to get set up.
4. Confirm config with `gmu sc`.
5. Run the Script and watch the magic happen.

   ```shell
   gmu dp
   ```

## Motivation (or Rationale)

As a current, part-time graduate student @ [George Mason](https://www.gmu.edu/), I usually take 1 class per semester,
and it's more cost-effective to purchase the Daily Permit, as opposed to a Weekly or Semester Permit.

However, purchasing a Daily Permit is a time-consuming process, and I usually procrastinate and leave it off till
the last minute (day of) which results in added stress on my part.

This Script aims to solve my longstanding issue, and enable me to more easily
purchase Daily Permit for the date of class.

## Fields

### Parking Date

Parking Date can be a weekday like `'Monday' 'Tuesday' 'Wednesday'`

or you could also hard-code the date: `October 10`
