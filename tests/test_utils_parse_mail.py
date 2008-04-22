#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cStringIO import StringIO
from DebianChangesBot.utils import parse_mail

class TestUtilsParseMail(unittest.TestCase):

    def testSimple(self):
        f = StringIO("""
From: Chris Lamb <chris@chris-lamb.co.uk>
Subject: This is the subject

Simple message body"""[1:])

        headers, body = parse_mail(f)

        self.assertEqual(headers['From'], u"Chris Lamb <chris@chris-lamb.co.uk>")
        self.assertEqual(headers['Subject'], u"This is the subject")
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0], u"Simple message body")

        self.assertEqual(type(headers['From']), unicode)
        self.assertEqual(type(headers['Subject']), unicode)
        self.assertEqual(type(body[0]), unicode)


    def testLongSubject(self):
        f = StringIO("""
From: Chris Lamb <chris@chris-lamb.co.uk>
Subject: Bug#123456: marked as done (pinafore: Inertial couplings may
 exceed tolerance when docking)

Simple message body"""[1:])

        headers, body = parse_mail(f)

        self.assertEqual(headers['Subject'], u"Bug#123456: marked as done " \
            "(pinafore: Inertial couplings may exceed tolerance when docking)")

    def testLongLine(self):
        f = StringIO("""
Subject: Subject

AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
"""[1:])

        headers, body = parse_mail(f)
        self.assertEqual(body[0], ('A' * 73) + ('B' * 73) + ('C' * 73))

    def testNotLongLine(self):
        f = StringIO("""
Subject: Subject

AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=
BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
"""[1:])

        headers, body = parse_mail(f)
        self.assertNotEqual(body, [('A' * 73) + ('B' * 73) + ('C' * 73)])

    def testSpaceAtEndOfLine(self):
        f = StringIO("""
Subject: Subject

Description:=20
"""[1:])

        headers, body = parse_mail(f)
        self.assertEqual(body, ['Description: '])

    def testUnicodeHeader(self):
        f = StringIO("""
From: Gon=C3=A9ri Le Bouder

Message body
"""[1:])

        headers, body = parse_mail(f)
        self.assertEqual(headers['From'], u"Gonéri Le Bouder")
        self.assertEqual(body, ['Message body'])

    def testUnicodeBody(self):
        f = StringIO("""
Subject: Subject line

Gon=C3=A9ri Le Bouder
"""[1:])
        headers, body = parse_mail(f)
        self.assertEqual(headers['Subject'], 'Subject line')
        self.assertEqual(body, [u"Gon=C3=A9ri Le Bouder"])

    def testUtf8Header(self):
        f = StringIO("""
From: Sebastian =?UTF-8?Q?Dr=C3=B6ge?=

Message body"""[1:])

        headers, body = parse_mail(f)
        self.assertEqual(headers['From'], u"Sebastian Dröge")
        self.assertEqual(body, ['Message body'])

    def testMultipart(self):
        f = StringIO("""
From: Mohammed Sameer <msameer@foolab.org>
To: Cristian Greco <cgreco@cs.unibo.it>
Cc: 402462@bugs.debian.org
Content-Type: multipart/signed; micalg=pgp-sha1;
	protocol="application/pgp-signature"; boundary="JlJsEFsx9RQyiX4C"
Content-Disposition: inline


--JlJsEFsx9RQyiX4C
Content-Type: text/plain; charset=utf-8
Content-Disposition: inline
Content-Transfer-Encoding: quoted-printable

On Sat, Apr 19, 2008 at 04:45:42PM +0200, Cristian Greco wrote:
> owner 402462 !
> thanks
>=20
> I'll work on this package, Mohammed Sameer agree with me because he is to=
o busy
> now.

Acknowledged.

--=20
GPG-Key: 0xA3FD0DF7 - 9F73 032E EAC9 F7AD 951F  280E CB66 8E29 A3FD 0DF7
Debian User and Developer.
Homepage: www.foolab.org

--JlJsEFsx9RQyiX4C
Content-Type: application/pgp-signature; name="signature.asc"
Content-Description: Digital signature
Content-Disposition: inline

-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.6 (GNU/Linux)

iD8DBQFICoPwy2aOKaP9DfcRAn7xAJ486L4EWnH/nL176FF4yZSoT2xKEACeNZX4
orkuFNMGzF2Qx9fiQRLWemE=
=ivv9
-----END PGP SIGNATURE-----

--JlJsEFsx9RQyiX4C--
"""[1:])

        headers, body = parse_mail(f)
        self.assert_(u"Acknowledged." in body)

if __name__ == "__main__":
    unittest.main()
