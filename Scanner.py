#-------------------------------------
#Scanner.py - The ATG file scanner.
#Compiler Generator Coco/R,
#Copyright (c) 1990, 2004 Hanspeter Moessenboeck, University of Linz
#extended by M. Loeberbauer & A. Woess, Univ. of Linz
#ported from Java to Python by Ronald Longo
#
#This program is free software; you can redistribute it and/or modify it
#under the terms of the GNU General Public License as published by the
#Free Software Foundation; either version 2, or (at your option) any
#later version.
#
#This program is distributed in the hope that it will be useful, but
#WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
#for more details.
#
#You should have received a copy of the GNU General Public License along
#with this program; if not, write to the Free Software Foundation, Inc.,
#59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
#As an exception, it is allowed to write an extension of Coco/R that is
#used as a plugin in non-free software.
#
#If not otherwise stated, any source code generated by Coco/R (other than
#Coco/R itself) does not fall under the GNU General Public License.
#-------------------------------------

import sys

class Token( object ):
   def __init__( self ):
      self.kind   = 0     # token kind
      self.pos    = 0     # token position in the source text (starting at 0)
      self.col    = 0     # token column (starting at 0)
      self.line   = 0     # token line (starting at 1)
      self.val    = u''   # token value
      self.next   = None  # AW 2003-03-07 Tokens are kept in linked list


class Position( object ):    # position of source code stretch (e.g. semantic action, resolver expressions)
   def __init__( self, buf, beg, len, col ):
      assert isinstance( buf, Buffer )
      assert isinstance( beg, int )
      assert isinstance( len, int )
      assert isinstance( col, int )
      
      self.buf = buf
      self.beg = beg   # start relative to the beginning of the file
      self.len = len   # length of stretch
      self.col = col   # column number of start position

   def getSubstring( self ):
      return self.buf.readPosition( self )

class Buffer( object ):
   EOF      = u'\u0100'     # 256

   def __init__( self, s ):
      self.buf    = s
      self.bufLen = len(s)
      self.pos    = 0
      self.lines  = s.splitlines( True )

   def Read( self ):
      if self.pos < self.bufLen:
         result = unichr(ord(self.buf[self.pos]) & 0xff)   # mask out sign bits
         self.pos += 1
         return result
      else:
         return Buffer.EOF

   def ReadChars( self, numBytes=1 ):
      result = self.buf[ self.pos : self.pos + numBytes ]
      self.pos += numBytes
      return result

   def Peek( self ):
      if self.pos < self.bufLen:
         return unichr(ord(self.buf[self.pos]) & 0xff)    # mask out sign bits
      else:
         return Scanner.buffer.EOF

   def getString( self, beg, end ):
      s = ''
      oldPos = self.getPos( )
      self.setPos( beg )
      while beg < end:
         s += self.Read( )
         beg += 1
      self.setPos( oldPos )
      return s

   def getPos( self ):
      return self.pos

   def setPos( self, value ):
      if value < 0:
         self.pos = 0
      elif value >= self.bufLen:
         self.pos = self.bufLen
      else:
         self.pos = value

   def readPosition( self, pos ):
      assert isinstance( pos, Position )
      self.setPos( pos.beg )
      return self.ReadChars( pos.len )

   def __iter__( self ):
      return iter(self.lines)

class Scanner(object):
   EOL     = u'\n'
   eofSym  = 0

   charSetSize = 256
   maxT = 48
   noSym = 48
   # terminals
   EOF_SYM = 0
   ident_Sym = 1
   number_Sym = 2
   string_Sym = 3
   badString_Sym = 4
   COMPILER_Sym = 5
   IGNORECASE_Sym = 6
   CHARACTERS_Sym = 7
   TOKENS_Sym = 8
   NAMES_Sym = 9
   PRAGMAS_Sym = 10
   COMMENTS_Sym = 11
   FROM_Sym = 12
   TO_Sym = 13
   NESTED_Sym = 14
   IGNORE_Sym = 15
   PRODUCTIONS_Sym = 16
   equal_Sym = 17
   point_Sym = 18
   END_Sym = 19
   plus_Sym = 20
   minus_Sym = 21
   pointpoint_Sym = 22
   ANY_Sym = 23
   CHR_Sym = 24
   lparen_Sym = 25
   rparen_Sym = 26
   less_Sym = 27
   uparrow_Sym = 28
   out_Sym = 29
   greater_Sym = 30
   comma_Sym = 31
   lesspoint_Sym = 32
   pointgreater_Sym = 33
   bar_Sym = 34
   WEAK_Sym = 35
   lbrack_Sym = 36
   rbrack_Sym = 37
   lbrace_Sym = 38
   rbrace_Sym = 39
   SYNC_Sym = 40
   IF_Sym = 41
   CONTEXT_Sym = 42
   lparenpoint_Sym = 43
   pointrparen_Sym = 44
   from_Sym = 45
   import_Sym = 46
   star_Sym = 47
   NOT_SYM = 48
   # pragmas
   ddtSym_Sym = 49

   start = [
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  6,  0,  5,  0,  0,  7, 29, 14, 27, 11, 17, 12, 28,  0,
     2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  0,  0, 30, 10, 16,  0,
     0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 21,  0, 22, 15,  0,
     0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,
     1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 23, 20, 24,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
     -1]


   def __init__( self, s ):
      self.buffer = Buffer( unicode(s) ) # the buffer instance
      
      self.ch        = u'\0'       # current input character
      self.pos       = -1          # column number of current character
      self.line      = 1           # line number of current character
      self.lineStart = 0           # start position of current line
      self.oldEols   = 0           # EOLs that appeared in a comment;
      self.NextCh( )
      self.ignore    = set( )      # set of characters to be ignored by the scanner
      self.ignore.add( ord(' ') )  # blanks are always white space
      self.ignore.add(9) 
      self.ignore.add(10) 
      self.ignore.add(13) 

      # fill token list
      self.tokens = Token( )       # the complete input token stream
      node   = self.tokens

      node.next = self.NextToken( )
      node = node.next
      while node.kind != Scanner.eofSym:
         node.next = self.NextToken( )
         node = node.next

      node.next = node
      node.val  = u'EOF'
      self.t  = self.tokens     # current token
      self.pt = self.tokens     # current peek token

   def NextCh( self ):
      if self.oldEols > 0:
         self.ch = Scanner.EOL
         self.oldEols -= 1
      else:
         self.ch = self.buffer.Read( )
         self.pos += 1
         # replace isolated '\r' by '\n' in order to make
         # eol handling uniform across Windows, Unix and Mac
         if (self.ch == u'\r') and (self.buffer.Peek() != u'\n'):
            self.ch = Scanner.EOL
         if self.ch == Scanner.EOL:
            self.line += 1
            self.lineStart = self.pos + 1
      



   def Comment0( self ):
      level = 1
      line0 = self.line
      lineStart0 = self.lineStart
      self.NextCh()
      if self.ch == '/':
         self.NextCh()
         while True:
            if ord(self.ch) == 10:
               level -= 1
               if level == 0:
                  self.oldEols = self.line - line0
                  self.NextCh()
                  return True
               self.NextCh()
            elif self.ch == Buffer.EOF:
               return False
            else:
               self.NextCh()
      else:
         if self.ch == Scanner.EOL:
            self.line -= 1
            self.lineStart = lineStart0
         self.pos = self.pos - 2
         self.buffer.setPos(self.pos+1)
         self.NextCh()
      return False

   def Comment1( self ):
      level = 1
      line0 = self.line
      lineStart0 = self.lineStart
      self.NextCh()
      if self.ch == '*':
         self.NextCh()
         while True:
            if self.ch == '*':
               self.NextCh()
               if self.ch == '/':
                  level -= 1
                  if level == 0:
                     self.oldEols = self.line - line0
                     self.NextCh()
                     return True
                  self.NextCh()
            elif self.ch == '/':
               self.NextCh()
               if self.ch == '*':
                  level += 1
                  self.NextCh()
            elif self.ch == Buffer.EOF:
               return False
            else:
               self.NextCh()
      else:
         if self.ch == Scanner.EOL:
            self.line -= 1
            self.lineStart = lineStart0
         self.pos = self.pos - 2
         self.buffer.setPos(self.pos+1)
         self.NextCh()
      return False


   def CheckLiteral( self ):
      lit = self.t.val
      if lit == "COMPILER":
         self.t.kind = Scanner.COMPILER_Sym
      elif lit == "IGNORECASE":
         self.t.kind = Scanner.IGNORECASE_Sym
      elif lit == "CHARACTERS":
         self.t.kind = Scanner.CHARACTERS_Sym
      elif lit == "TOKENS":
         self.t.kind = Scanner.TOKENS_Sym
      elif lit == "NAMES":
         self.t.kind = Scanner.NAMES_Sym
      elif lit == "PRAGMAS":
         self.t.kind = Scanner.PRAGMAS_Sym
      elif lit == "COMMENTS":
         self.t.kind = Scanner.COMMENTS_Sym
      elif lit == "FROM":
         self.t.kind = Scanner.FROM_Sym
      elif lit == "TO":
         self.t.kind = Scanner.TO_Sym
      elif lit == "NESTED":
         self.t.kind = Scanner.NESTED_Sym
      elif lit == "IGNORE":
         self.t.kind = Scanner.IGNORE_Sym
      elif lit == "PRODUCTIONS":
         self.t.kind = Scanner.PRODUCTIONS_Sym
      elif lit == "END":
         self.t.kind = Scanner.END_Sym
      elif lit == "ANY":
         self.t.kind = Scanner.ANY_Sym
      elif lit == "CHR":
         self.t.kind = Scanner.CHR_Sym
      elif lit == "out":
         self.t.kind = Scanner.out_Sym
      elif lit == "WEAK":
         self.t.kind = Scanner.WEAK_Sym
      elif lit == "SYNC":
         self.t.kind = Scanner.SYNC_Sym
      elif lit == "IF":
         self.t.kind = Scanner.IF_Sym
      elif lit == "CONTEXT":
         self.t.kind = Scanner.CONTEXT_Sym
      elif lit == "from":
         self.t.kind = Scanner.from_Sym
      elif lit == "import":
         self.t.kind = Scanner.import_Sym


   def NextToken( self ):
      while ord(self.ch) in self.ignore:
         self.NextCh( )
      if (self.ch == '/' and self.Comment0() or self.ch == '/' and self.Comment1()):
         return self.NextToken()

      self.t = Token( )
      self.t.pos = self.pos
      self.t.col = self.pos - self.lineStart + 1
      self.t.line = self.line
      state = self.start[ord(self.ch)]
      buf = u''
      buf += unicode(self.ch)
      self.NextCh()

      done = False
      while not done:
         if state == -1:
            self.t.kind = Scanner.eofSym     # NextCh already done
            done = True
         elif state == 0:
            self.t.kind = Scanner.noSym      # NextCh already done
            done = True
         elif state == 1:
            if (self.ch >= '0' and self.ch <= '9'
                 or self.ch >= 'A' and self.ch <= 'Z'
                 or self.ch >= 'a' and self.ch <= 'z'):
               buf += unicode(self.ch)
               self.NextCh()
               state = 1
            else:
               self.t.kind = Scanner.ident_Sym
               self.t.val = buf
               self.CheckLiteral()
               return self.t
         elif state == 2:
            if (self.ch >= '0' and self.ch <= '9'):
               buf += unicode(self.ch)
               self.NextCh()
               state = 2
            else:
               self.t.kind = Scanner.number_Sym
               done = True
         elif state == 3:
            self.t.kind = Scanner.string_Sym
            done = True
         elif state == 4:
            self.t.kind = Scanner.badString_Sym
            done = True
         elif state == 5:
            if (self.ch >= '0' and self.ch <= '9'
                 or self.ch >= 'A' and self.ch <= 'Z'
                 or self.ch >= 'a' and self.ch <= 'z'):
               buf += unicode(self.ch)
               self.NextCh()
               state = 5
            else:
               self.t.kind = Scanner.ddtSym_Sym
               done = True
         elif state == 6:
            if (ord(self.ch) <= 9
                 or ord(self.ch) >= 11 and ord(self.ch) <= 12
                 or ord(self.ch) >= 14 and self.ch <= '!'
                 or self.ch >= '#' and self.ch <= '['
                 or self.ch >= ']' and ord(self.ch) <= 255):
               buf += unicode(self.ch)
               self.NextCh()
               state = 6
            elif (ord(self.ch) == 10
                 or ord(self.ch) == 13):
               buf += unicode(self.ch)
               self.NextCh()
               state = 4
            elif self.ch == '"':
               buf += unicode(self.ch)
               self.NextCh()
               state = 3
            elif ord(self.ch) == 92:
               buf += unicode(self.ch)
               self.NextCh()
               state = 8
            else:
               self.t.kind = Scanner.noSym
               done = True
         elif state == 7:
            if (ord(self.ch) <= 9
                 or ord(self.ch) >= 11 and ord(self.ch) <= 12
                 or ord(self.ch) >= 14 and self.ch <= '&'
                 or self.ch >= '(' and self.ch <= '['
                 or self.ch >= ']' and ord(self.ch) <= 255):
               buf += unicode(self.ch)
               self.NextCh()
               state = 7
            elif (ord(self.ch) == 10
                 or ord(self.ch) == 13):
               buf += unicode(self.ch)
               self.NextCh()
               state = 4
            elif ord(self.ch) == 39:
               buf += unicode(self.ch)
               self.NextCh()
               state = 3
            elif ord(self.ch) == 92:
               buf += unicode(self.ch)
               self.NextCh()
               state = 9
            else:
               self.t.kind = Scanner.noSym
               done = True
         elif state == 8:
            if (self.ch >= ' ' and self.ch <= '~'):
               buf += unicode(self.ch)
               self.NextCh()
               state = 6
            else:
               self.t.kind = Scanner.noSym
               done = True
         elif state == 9:
            if (self.ch >= ' ' and self.ch <= '~'):
               buf += unicode(self.ch)
               self.NextCh()
               state = 7
            else:
               self.t.kind = Scanner.noSym
               done = True
         elif state == 10:
            self.t.kind = Scanner.equal_Sym
            done = True
         elif state == 11:
            self.t.kind = Scanner.plus_Sym
            done = True
         elif state == 12:
            self.t.kind = Scanner.minus_Sym
            done = True
         elif state == 13:
            self.t.kind = Scanner.pointpoint_Sym
            done = True
         elif state == 14:
            self.t.kind = Scanner.rparen_Sym
            done = True
         elif state == 15:
            self.t.kind = Scanner.uparrow_Sym
            done = True
         elif state == 16:
            self.t.kind = Scanner.greater_Sym
            done = True
         elif state == 17:
            self.t.kind = Scanner.comma_Sym
            done = True
         elif state == 18:
            self.t.kind = Scanner.lesspoint_Sym
            done = True
         elif state == 19:
            self.t.kind = Scanner.pointgreater_Sym
            done = True
         elif state == 20:
            self.t.kind = Scanner.bar_Sym
            done = True
         elif state == 21:
            self.t.kind = Scanner.lbrack_Sym
            done = True
         elif state == 22:
            self.t.kind = Scanner.rbrack_Sym
            done = True
         elif state == 23:
            self.t.kind = Scanner.lbrace_Sym
            done = True
         elif state == 24:
            self.t.kind = Scanner.rbrace_Sym
            done = True
         elif state == 25:
            self.t.kind = Scanner.lparenpoint_Sym
            done = True
         elif state == 26:
            self.t.kind = Scanner.pointrparen_Sym
            done = True
         elif state == 27:
            self.t.kind = Scanner.star_Sym
            done = True
         elif state == 28:
            if self.ch == '.':
               buf += unicode(self.ch)
               self.NextCh()
               state = 13
            elif self.ch == '>':
               buf += unicode(self.ch)
               self.NextCh()
               state = 19
            elif self.ch == ')':
               buf += unicode(self.ch)
               self.NextCh()
               state = 26
            else:
               self.t.kind = Scanner.point_Sym
               done = True
         elif state == 29:
            if self.ch == '.':
               buf += unicode(self.ch)
               self.NextCh()
               state = 25
            else:
               self.t.kind = Scanner.lparen_Sym
               done = True
         elif state == 30:
            if self.ch == '.':
               buf += unicode(self.ch)
               self.NextCh()
               state = 18
            else:
               self.t.kind = Scanner.less_Sym
               done = True

      self.t.val = buf
      return self.t

   def Scan( self ):
      self.t = self.t.next
      self.pt = self.t.next
      return self.t

   def Peek( self ):
      self.pt = self.pt.next
      while self.pt.kind > self.maxT:
         self.pt = self.pt.next

      return self.pt

   def ResetPeek( self ):
      self.pt = self.t

