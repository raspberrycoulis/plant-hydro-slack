# plant-hydro-slack
Using a Raspberry Pi and a soil moisture sensor to send Slack notifications when our plant needs watering. This is based on [ModMyPi's code](https://www.modmypi.com/blog/raspberry-pi-plant-pot-moisture-sensor-with-email-notification-tutorial) but adapted to send Slack notifications instead.

## Required parts:
* A Raspberry Pi (I used a Pi Zero W for convenience)
* A soil moisture sensor (available at [ModMyPi](https://www.modmypi.com/electronics/sensors-347/soil-moisture-sensor/?r=raspberrycoulis) and on [eBay](https://www.ebay.co.uk/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313.TR0.TRC0.H0.Xsoil+moisture+sensor.TRS0&_nkw=soil+moisture+sensor&_sacat=0)
* A [Slack](https://slack.com/) account
* A [webhook intergation](https://api.slack.com/custom-integrations/incoming-webhooks)
* This code.

## Connect the soil moisture sensor
This is very simple. There are two connections on the fork shaped part (that goes into the soil) marked positive and negative - simply connect these to the sensor module part. It doesn't matter which of the two pins you use. Whilst there are 4 pins on the part of the sensor module that connects to your Raspberry Pi, you only need 3: VCC, GND and D0. Connect these as follows:
* VCC to pin 1 on the Pi (3.3v)
* GND to pin 9 on the Pi (Ground)
* D0 to pin 11 on the Pi (GPIO 17).

If connected corrrectly, you should see at least 1 LED light up on the sensor module. If you then stick the fork end into a glass of water (only the prongs, not the entire module!), you should then see a second LED light up on the sensor module. If you don't, go back and check your connections - try swapping the two from the fork to the sensor module around first.

### Calibrate the soil moisture sensor
There is a small potentiometer on the sensor module that allows you to calibrate the sensitivity of the sensor. The best way to do this is to insert the prongs of the fork into the soil and then slowly turn the potentiometer until 1 LED goes off, this means that when the soil moisture drops to this level, the script will be triggered and alert you via Slack that it needs watering.

## Clone this GitHub repo
Obviously you'll need the code, so clone this on your Raspberry Pi by running this in your command line:
```
$ git clone git://github.com/raspberrycoulis/plant-hydro-slack.git
```

## Edit the code to include your Slack webhook
After you have created your webhook integration in Slack, you'll need to edit the Python script accordingly:
```
$ cd plant-hydro-slack
$ nano dry-to-slack.py
```
Find the variable on line 20 called `webhook_url` and then replace `"ADD_HERE"` with your Slack webhook URL. Then save and exit:
```
$ CTRL+X
$ Y
```
Your script is now good to go.

## Running the script automatically on boot using systemd
In order to run the script automatically when the Raspberry Pi boots, I recommend using systemd to run it as a service:

```
$ sudo nano /lib/systemd/system/moisturesensor.service
```

Then add the following:

```
[Unit]
Description=Plant soil moisture sensor service
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python /home/pi/plant-hydro-slack/dry-to-slack.py > /home/pi/plant-hydro-slack/dry-to-slack.log 2>&1
Restart=always

[Install]
WantedBy=multi-user.target
```

The parts to check are the `ExecStart` command as this assumes the `dry-to-slack.py` script is located in `/home/pi/plant-hydro-slack` so please update accordingly if you have installed the script in a different location.

Once you have done this, `Ctrl+X` to exit and `Y` to save then run:

```
$ sudo chmod 644 /lib/systemd/system/moisturesensor.service
$ sudo systemctl daemon-reload
$ sudo systemctl enable moisturesensor.service
```

You can `sudo reboot` or simply run `sudo systemctl start moisturesensor.service` to start the script. Check the status by running `sudo systemctl status moisturesensor.service`.
