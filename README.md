# M-numbers calculator

This is my implementation of M-number expression parser and calculator web application. This was made possible with a bulk of code from professor Mario Essert.
The GUI was developed by @amalija-ramljak.

## Deployment
```bash
python3 -m venv venv                        # always use venv
source venv/bin/activate                    # ALWAYS
pip install -r requirements.txt
FLASK_APP=app.py flask run -h ${YOUR_HOST} -p ${YOUR_PORT}
```

## Explanation
In short, a new type of mathematical structure is being investigated after an invention/discovery by Miroslav Šare in 1970's. They are called M-numbers and they stem from electrical circuits. M-numbers are a special form of summary of electrical scheme topology. More info about this is TBA as the materials (in English) and science papers are in the work.

Croatian language version is already available.

English version can be found [overhere](https://amas.pmfst.unist.hr/uploads/61/AMAS_21_02_revised_v2.pdf)

For more info, see [this page for contact information](https://www.fer.unizg.hr/en/course/mnu).
