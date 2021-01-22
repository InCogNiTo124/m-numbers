from mnums import MBRParser, MBRTransformer
import string

def test_parser_abc(parser):
    assert parser.parse("D(a)") == "c"
    assert parser.parse("D(b)") == "b"
    assert parser.parse("delta(a, c)") == 2
    assert parser.parse("len_s(abcbac)") == -2
    assert parser.parse("len_p(abcbac)") == 0
    assert parser.parse("len(abcbac)") == -2
    assert parser.parse("left(abcbac)") == "a"
    assert parser.parse("right(abcbac)") == "c"
    assert parser.parse("left_d(abcbac)") == parser.parse("D(left(abcbac))") == "c"
    assert parser.parse("right_d(abcbac)") == parser.parse("D(right(abcbac))") == "a"
    assert parser.parse("zip(abcbac)") == "ac"
    assert parser.parse("Q(abcbac)") == "ac"
    assert parser.parse("E(abcbac)") == "cabcba"
    assert parser.parse("I(abcbac)") == "aabcbacc"
    assert parser.parse("K(abcbac)") == "cabcbaca"
    assert parser.parse("F(abcbac)") == "acbabc"
    assert parser.parse("G(abcbac)") == "cabcbaca"
    assert parser.parse("H(abcbac)") == "aabcbacc"
    assert parser.parse("Io(abcbac)") == "acabcbac"
    assert parser.parse("J_s(abcbac)") == "caabcbacca"
    assert parser.parse("J_p(abcbac)") == "acabcbacac" 
    assert parser.parse("Q_s(abcbac)") == "aacc"
    assert parser.parse("Q_p(abcbac)") == "acac"
    assert parser.parse("I_s(abcbac)") == "aabcbaccaacc"
    assert parser.parse("I_p(abcbac)") == "accabcbacc"
    assert parser.parse("E_s(abcbac)") == "caabcbacca"
    assert parser.parse("E_p(abcbac)") == "ccabcbacaa"
    assert parser.parse("D_s(abcbac)") == "caacbabcca"
    assert parser.parse("D_p(abcbac)") == "ccacbabcaa"
    assert parser.parse("K_s(abcbac)") == "cabcbacc"
    assert parser.parse("K_p(abcbac)") == "aabcbaca"
    assert parser.parse("PS(abcbac, abcbca)") == "aaabcbacacabcbcaaa" 
    assert parser.parse("SS(abcbac, abcbca)") == "aaabcbaccaabcbcacc"
    assert parser.parse("PO(abcbac, abcbca)") == "aaabcbacacaaaabcbcaaaa"
    assert parser.parse("SO(abcbac, abcbca)") == "aaabcbaccaaabcbcaaaaaacc"
    assert parser.parse("PM(abcbac, 2)") == parser.parse("PS(abcbac, abcbac)")
    assert parser.parse("PM(abcbac, 3)") == "aaaaabcbacacabcbacccacabcbaccc"
    assert parser.parse("SM(abcbac, 2)") == parser.parse("SS(abcbac, abcbac)")
    assert parser.parse("SM(abcbac, 3)") == "aaaaabcbaccaabcbaccccaabcbaccc"
    assert parser.parse("SI(abcbac, abcbca)") == "aacabcbacaaaabcbcaaa" 
    assert parser.parse("PI(abcbac, abcbca)") == "cccabcbacaaaabcbcaaa"
    assert parser.parse("SE(abcbac, abcbca)") == "aaaacabcbacaaaabcbcaaaaaaacabcbcaccaabcbacccaa"
    assert parser.parse("PE(abcbac, abcbca)") == "cccccabcbacaaaabcbcaaacacccabcbcacacabcbaccccc"
    return

def test_parser_ascii(parser):
    assert parser.parse("D(a)") == "z"
    assert parser.parse("D(y)") == "b"
    assert parser.parse("delta(a, c)") == 2
    assert parser.parse("len_s(ac)") == -2
    assert parser.parse("len_p(abcbac)") == 0
    assert parser.parse("len(abcbac)") == -2
    assert parser.parse("left(abcbac)") == "a"
    assert parser.parse("right(abcbac)") == "c"
    assert parser.parse("left_d(abcbac)") == parser.parse("D(left(abcbac))") == "z"
    assert parser.parse("right_d(abcbac)") == parser.parse("D(right(abcbac))") == "x"
    assert parser.parse("zip(abcbac)") == "ac"
    assert parser.parse("Q(abcbac)") == "ac"
    assert parser.parse("E(abcbac)") == "cabcba"
    assert parser.parse("I(abcbac)") == "aabcbacc"
    assert parser.parse("K(abcbac)") == "zabcbacx"
    assert parser.parse("F(abcbac)") == "xzyxyz"
    assert parser.parse("G(abcbac)") == "cabcbaca"
    assert parser.parse("H(abcbac)") == "xabcbacz"
    assert parser.parse("Io(abcbac)") == "acabcbac"
    assert parser.parse("J_s(abcbac)") == "zaabcbacza"
    assert parser.parse("J_p(abcbac)") == "azabcbacaz"
    assert parser.parse("Q_s(abcbac)") == "aacc"
    assert parser.parse("Q_p(abcbac)") == "acac"
    assert parser.parse("I_s(abcbac)") == "aabcbaccaacc"
    assert parser.parse("I_p(abcbac)") == "accabcbacc"
    assert parser.parse("E_s(abcbac)") == "caabcbacca"
    assert parser.parse("E_p(abcbac)") == "ccabcbacaa"
    assert parser.parse("D_s(abcbac)") == "zxxzyxyzzx"
    assert parser.parse("D_p(abcbac)") == "zzxzyxyzxx"
    assert parser.parse("K_s(abcbac)") == "zabcbacz"
    assert parser.parse("K_p(abcbac)") == "aabcbaca"
    assert parser.parse("PS(abcbac, abcbca)") == "aaabcbacacabcbcaaa" 
    assert parser.parse("SS(abcbac, abcbca)") == "aaabcbaccaabcbcacc"
    assert parser.parse("PO(abcbac, abcbca)") == "aaabcbacacaaaabcbcaaaa"
    assert parser.parse("SO(abcbac, abcbca)") == "aaabcbaccaaabcbcaaaaaacc"
    assert parser.parse("PM(abcbac, 2)") == parser.parse("PS(abcbac, abcbac)")
    assert parser.parse("PM(abcbac, 3)") == "aaaaabcbacacabcbacccacabcbaccc"
    assert parser.parse("SM(abcbac, 2)") == parser.parse("SS(abcbac, abcbac)")
    assert parser.parse("SM(abcbac, 3)") == "aaaaabcbaccaabcbaccccaabcbaccc"
    assert parser.parse("SI(abcbac, abcbca)") == "aazabcbacxxaabcbcaxx"
    assert parser.parse("PI(abcbac, abcbca)") == "zzzabcbacxaxabcbcaaa"
    assert parser.parse("SE(abcbac, abcbca)") == "aaaazabcbacxxaabcbcaxxaxaazabcbcazzaabcbaczzxx"
    assert parser.parse("PE(abcbac, abcbca)") == "zzzzzabcbacxaxabcbcaaazazzzabcbcazazabcbaccccc"
    return

if __name__ == "__main__":
    parser = MBRParser("abc", MBRTransformer())
    test_parser_abc(parser)
    parser.set_alphabet(string.ascii_lowercase)
    test_parser_ascii(parser)
