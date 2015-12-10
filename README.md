# Private Easy Uploader

[![Build Status](https://img.shields.io/travis/jtwp470/private-easy-uploader.svg?style=flat-square)](https://travis-ci.org/jtwp470/private-easy-uploader)
[![License](http://img.shields.io/:license-mit-blue.svg)](http://jtwp470.mit-license.org/)

**Private Easy Uploader** (aka. PE uploader) is own uploader system using Flask and Python environment.
This application will provide simple function for me.

*PE uploader is under development.* Please wait stable release.

#### Functions

* [x] File uploading and publishing
* [ ] Simple access control
* [ ] Add tag and search
* [ ] [FUTURE] Link to [Amazon S3](https://aws.amazon.com/s3/?nc1=h_ls)

## How to deploy & run

1. Please install Python (>= 3.4) on your machine. (:apple: `brew install python3`)
2. Clone this repository.
3. Install `pip` or use `virtualenv` like this: `virtualenv .`
4. Install dependences like this: `pip install -r requirements.txt`
5. Initialize database: `python manage.py init_db`
6. Run app: `python manage.py runserver` (After access `http://localhost:5000`)
7. Setup admin account to use. Please access `http://localhost:5000/admin/add` and login server.
8. Please enjoy!

## For developer
TODO

## Security Issue
Please report security issue to <del>my twitter account([@jtwp470](https://twitter.com/jtwp470)) or</del> E-mail.

There is my Email address on my GitHub top page.

## License
This project is under MIT license. Please refer to [LICENSE](./LICENSE) to see more details.
