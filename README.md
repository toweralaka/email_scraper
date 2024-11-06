# Email Scraper
Python script to access email, download files and extract data

## Setting up a development environment

1. Have Python 3
2. Create a virtualenv:
   ```console
   $ python3 -m venv the_env
   ```
3. Activate the venv:
   ```console
   $ . the_env/bin/activate  # or a Windows alternative
   ```
   *Note that you have to run this every time you start a new
   terminal shell session.*
4. Run the following to have the same requirements installed in your local virtualenv you've just activated:
   ```console
   $ pip install -r requirements.txt
   ```
5. Set up "dotenv" by copying the example file and altering the values:
   ```console
   $ cp -v .env{.example,.}
   $ Update .env file with correct credentials

## To Automate
1. Open `cron` file
    ```console
    $ crontab -e
    ```
2. Add cron job
    ```console
    0 11 * * * /usr/bin/python3 /path/to/your/script.py
    ```

    - This runs your script `script.py` at 11 a.m. everyday.
        - `* * * * *`
        - minute
        (0-59)
        - hour
        (0-23)
        - day of the month
        (1-31)
        - month
        (1-12) (or JAN-DEC)
        - day of the week
        (0-7) (or MON-SUN)

    - Visit [https://www.uptimia.com/cron-expression-generator](https://www.uptimia.com/cron-expression-generator) to generate cron.

3. Save file and close