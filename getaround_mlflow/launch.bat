docker run -it -v "%cd%":/home/app -p 4000:80 -e PORT=80 -e AWS_ACCESS_KEY_ID=AKIAUPXUR63L25HEOPHA -e AWS_SECRET_ACCESS_KEY=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 -e BACKEND_STORE_URI=postgresql://avawfkylyjrphx:61a91302ae3320d6d94b867ff2d474754f58a3466eb2e3244140c81872fa01dc@ec2-3-217-146-37.compute-1.amazonaws.com:5432/dc1i7l944ogagv -e ARTIFACT_STORE_URI=s3://mlflow-getaround-bucket/getaround/ mlflow_getaround python app_mlflow.py

