import time

from parsimonious.grammar import Grammar
from parsimonious import NodeVisitor

from semanticversionrange import SemanticVersionComparator, SemanticVersionRange

class VersionRangeParser(object):
    def parse(self, version_range_str):
        print(version_range_str)

class NodeVersionRangeParser(VersionRangeParser):
    grammar = Grammar(r"""
        range_set   = range (logical_or range)*
        logical_or  = " "* "||" " "*
        range       = hyphen / (simple (" " simple)*) / ""
        hyphen      = hpart1 " - " hpart2
        hpart1      = partial ""
        hpart2      = partial ""
        simple      = primitive / partial
        primitive   = operator " "* partial
        operator    = ">=" / "<=" / "=" / "<" / ">" / "~" / "^"
        partial     = ver_num qualifier?
        ver_num     = xr ("." xr ("." xr)?)?   
        xr          = "x" / "X" / "*" / "latest" / nr
        nr          = "0" / (~"[1-9]" (~"[0-9]")*)
        qualifier   = ("-" pre)? ("+" build )?
        pre         = parts ""
        build       = parts ""
        parts       = part ("." part)*
        part        = nr / ~"[a-z0-9]"+
        """)

    def parse(self, version_range_str):
        tree = self.grammar.parse(version_range_str)

        vv = NodeVersionRangeVisitor()
        simples, hyphens = vv.get_simples_and_hyphens(tree)

        svr = SemanticVersionRange()
        for s in simples:
            svc = SemanticVersionComparator(s)
            svr.addComparatorToRange(svc)

        for h in hyphens:
            svc = SemanticVersionComparator(h)
            svr.addComparatorToRange(svc)

        return svr

class NodeVersionRangeVisitor(NodeVisitor):
    def __init__(self):
        self.partial = None
        self.operator = None
        self.simple = None
        self.range = None
        self.hyphen = None
        self.pre = None
        self.build = None
        self.ver_num = None
        self.hpart1 = None
        self.hpart2 = None
        self.logical_or = 0

        self.simples = []
        self.hyphens = []

    def get_simples_and_hyphens(self, tree):
        self.visit(tree)

        return self.simples, self.hyphens

    def visit_hpart1(self, node, children):
        if self.hpart1 != node.text:
            self.hpart1 = node.text
    def visit_hpart2(self, node, children):
        if self.hpart2 != node.text:
            self.hpart2 = node.text
    def visit_ver_num(self, node, children):
        if self.ver_num != node.text:
            self.ver_num = node.text
    def visit_pre(self, node, children):
        if self.pre != node.text:
            self.pre = node.text
    def visit_build(self, node, children):
        if self.build != node.text:
            self.build = node.text
    def visit_partial(self, node, children):
        if self.partial != node.text:
            self.partial = node.text
    def visit_operator(self, node, children):
        if self.operator != node.text:
            self.operator = node.text
    def visit_logical_or(self, node, children):
        if self.operator != node.text:
            self.logical_or = self.logical_or + 1

    def visit_range(self, node, children):
        if self.range != node.text:
            self.range = node.text

    def visit_simple(self, node, children):
        if self.simple != node.text:
            self.simple = node.text

            self.simples.append({"simple":self.simple, "operator":self.operator, "logical_or": self.logical_or, \
                                 "ver_num":self.ver_num, "pre": self.pre, "build": self.build})

    def visit_hyphen(self, node, children):
        if self.hyphen != node.text:
            self.hyphen = node.text

            self.hyphens.append({"hyphen":self.hyphen, "part1": self.hpart1, "part2": self.hpart2, \
                                 "logical_or": self.logical_or,})

    def generic_visit(self, node, visited_children):
        return node