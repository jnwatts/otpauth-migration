Steps:
1. Generate QR codes from Google Authenticator and save/read them (take picture w/ 2nd phone, webcam, etc)
2. Convert QR codes to text and concatenate (should be a very long string like `otpauth-migration://offline?data=...`)
```sh
for f in *.jpg; do
	zbarimg ${f} > ${f}.txt
done
cat *.jpg.txt > secrets.0
```
3. Decode data to verbose text
```sh
cat secrets.0 | sed 's/QR-Code://' | \
        sed 's/otpauth-migration:\/\/offline?data=//' | \
	sed -e 's/%2B/+/ig' -e 's/%2F/\//ig' -e 's/%3D/=/ig' | \
	base64 -d | \
	protoc --decode=MigrationPayload ./OtpMigration.proto > secrets.1
```
4. Take the opportunity to clean up crappy naming ;-)
5. Convert verbose text to otp-auth:// urls using provided python
```sh
python3 ./secrets.py < secrets.1 > secrets.2
```
6. Import secrets.2 in to [Numberstation](https://sr.ht/~martijnbraam/numberstation/) or any other client of your choosing
7. Clean up! Don't leave your secrets laying around ;-)

# Links
The above was assembled/congealed from bits of the following: (and a few others I've forgotten?)

- https://github.com/krissrex/google-authenticator-exporter
- https://github.com/qistoph/otp_export
- https://www.ctrl.blog/entry/google-authenticator-2fa-secrets.html
- https://github.com/google/google-authenticator/wiki/Key-Uri-Format
- https://sr.ht/~martijnbraam/numberstation/
