# https://deliciousbrains.com/ssl-certificate-authority-for-local-https-development/
set -x
subj="/C=US/ST=Massachuetts/L=Boston/O=CORS Demo/CN=cors.local"
openssl genrsa -des3 -out certificate_authority.key 2048
openssl req -x509 -new -nodes -key certificate_authority.key -sha256 -days 365 -subj "${subj}" -out certificate_authority.pem
openssl genrsa -out site.key 2048
openssl req -new -key site.key -out site.csr -subj "${subj}"
echo -e "authorityKeyIdentifier=keyid,issuer\n\
basicConstraints=CA:FALSE\n\
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment\n\
subjectAltName = @alt_names\n\
\n\
[alt_names]\n\
DNS.1 = cors.local" > site.ext
openssl x509 -req -in site.csr -CA certificate_authority.pem -CAkey certificate_authority.key \
-CAcreateserial -out site.crt -days 365 -sha256 -extfile site.ext

echo "Use site.crt and site.key with your http server"
echo "Add certificate_authority.pem to the System certificates in Keychain Access"
