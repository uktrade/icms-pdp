from web.auth.fox_hasher import FOXPBKDF2SHA1Hasher


class Test:
    def test_(self):
        result = FOXPBKDF2SHA1Hasher().encode('P4$$word', '3333:3F47482FD712BF0A', 10000)
        assert result == 'fox_pbkdf2_sha1$10000$3333_3F47482FD712BF0A$4051D4D9A0C5AA6845BD9A03E348FB2B'
