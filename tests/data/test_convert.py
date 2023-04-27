import json

import pytest
from lxml import etree

from doctree.data.definition import RootNode, HeadingNode, TextNode, NodeType
from doctree.data.convert import (
    line_reorder,
    convert_html_string_with_xfix,
    convert_html_to_line_json,
    convert_node_to_html,
    convert_to_universal_format,
    convert_to_universal_format_with_xfix,
    convert_json_to_node,
)


def test_parse():
    html_content2 = r"""<html xmlns:v="urn:schemas-microsoft-com:vml"
xmlns:o="urn:schemas-microsoft-com:office:office"
xmlns:w="urn:schemas-microsoft-com:office:word"
xmlns:dt="uuid:C2F41010-65B3-11d1-A29F-00AA00C14882"
xmlns:m="http://schemas.microsoft.com/office/2004/12/omml"
xmlns="http://www.w3.org/TR/REC-html40">

<head>
<meta http-equiv=Content-Type content="text/html; charset=gb2312">
<meta name=ProgId content=Word.Document>
<meta name=Generator content="Microsoft Word 15">
<meta name=Originator content="Microsoft Word 15">
<link rel=File-List href="12.files/filelist.xml">
<title>天海防务：关于开展商品期货套期保值业务的可行性分析报告</title>
<!--[if gte mso 9]><xml>
 <o:DocumentProperties>
  <o:Author>rjf</o:Author>
  <o:LastAuthor>rjf</o:LastAuthor>
  <o:Revision>2</o:Revision>
  <o:TotalTime>8</o:TotalTime>
  <o:Created>2021-10-27T12:50:00Z</o:Created>
  <o:LastSaved>2021-10-27T12:50:00Z</o:LastSaved>
  <o:Pages>1</o:Pages>
  <o:Words>435</o:Words>
  <o:Characters>2481</o:Characters>
  <o:Paragraphs>en</o:Paragraphs>
  <o:Lines>20</o:Lines>
  <o:Paragraphs>5</o:Paragraphs>
  <o:CharactersWithSpaces>2911</o:CharactersWithSpaces>
  <o:Version>16.00</o:Version>
 </o:DocumentProperties>
 <o:CustomDocumentProperties>
  <o:viewport dt:dt="string">width=device-width, initial-scale=1,minimum-scale=1</o:viewport>
 </o:CustomDocumentProperties>
 <o:OfficeDocumentSettings>
  <o:AllowPNG/>
 </o:OfficeDocumentSettings>
</xml><![endif]-->
<link rel=themeData href="12.files/themedata.thmx">
<link rel=colorSchemeMapping href="12.files/colorschememapping.xml">
<!--[if gte mso 9]><xml>
 <w:WordDocument>
  <w:SpellingState>Clean</w:SpellingState>
  <w:GrammarState>Clean</w:GrammarState>
  <w:TrackMoves>false</w:TrackMoves>
  <w:TrackFormatting/>
  <w:PunctuationKerning/>
  <w:DrawingGridHorizontalSpacing>18 磅</w:DrawingGridHorizontalSpacing>
  <w:DrawingGridVerticalSpacing>18 磅</w:DrawingGridVerticalSpacing>
  <w:DisplayHorizontalDrawingGridEvery>0</w:DisplayHorizontalDrawingGridEvery>
  <w:DisplayVerticalDrawingGridEvery>0</w:DisplayVerticalDrawingGridEvery>
  <w:ValidateAgainstSchemas/>
  <w:SaveIfXMLInvalid>false</w:SaveIfXMLInvalid>
  <w:IgnoreMixedContent>false</w:IgnoreMixedContent>
  <w:AlwaysShowPlaceholderText>false</w:AlwaysShowPlaceholderText>
  <w:DoNotPromoteQF/>
  <w:LidThemeOther>EN-US</w:LidThemeOther>
  <w:LidThemeAsian>ZH-CN</w:LidThemeAsian>
  <w:LidThemeComplexScript>X-NONE</w:LidThemeComplexScript>
  <w:Compatibility>
   <w:BreakWrappedTables/>
   <w:SnapToGridInCell/>
   <w:WrapTextWithPunct/>
   <w:UseAsianBreakRules/>
   <w:UseWord2010TableStyleRules/>
   <w:DontGrowAutofit/>
   <w:SplitPgBreakAndParaMark/>
   <w:UseFELayout/>
  </w:Compatibility>
  <w:DoNotOptimizeForBrowser/>
  <m:mathPr>
   <m:mathFont m:val="Cambria Math"/>
   <m:brkBin m:val="before"/>
   <m:brkBinSub m:val="&#45;-"/>
   <m:smallFrac m:val="off"/>
   <m:dispDef m:val="off"/>
   <m:lMargin m:val="0"/>
   <m:rMargin m:val="0"/>
   <m:defJc m:val="centerGroup"/>
   <m:wrapRight/>
   <m:intLim m:val="subSup"/>
   <m:naryLim m:val="subSup"/>
  </m:mathPr></w:WordDocument>
</xml><![endif]--><!--[if gte mso 9]><xml>
 <w:LatentStyles DefLockedState="false" DefUnhideWhenUsed="false"
  DefSemiHidden="false" DefQFormat="false" LatentStyleCount="375">
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="heading 6"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="index 3"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="index 4"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="index 5"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="index 6"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="index 7"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="index 8"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="index 9"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="toc 1"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="toc 2"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="toc 3"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="toc 4"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="toc 5"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="toc 6"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="toc 7"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="toc 8"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="toc 9"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Normal Indent"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="footnote text"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="annotation text"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="header"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="footer"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="index heading"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="caption"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="table of figures"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="envelope address"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="envelope return"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="footnote reference"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="annotation reference"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="line number"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="page number"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="endnote reference"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="endnote text"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="table of authorities"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="macro"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="toa heading"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="List"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="List Bullet"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="List Number"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="List 2"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="List 3"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="List 4"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="List 5"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="List Bullet 3"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="List Bullet 4"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="List Number 3"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="List Number 4"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="List Number 5"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Closing"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Signature"/>
  <w:LsdException Locked="false" Priority="1" SemiHidden="true"
   UnhideWhenUsed="true" Name="Default Paragraph Font"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Body Text"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Body Text Indent"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="List Continue"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="List Continue 2"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="List Continue 3"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="List Continue 4"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="List Continue 5"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Message Header"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Salutation"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Date"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Body Text First Indent"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Body Text First Indent 2"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Body Text Indent 3"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Block Text"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Hyperlink"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="FollowedHyperlink"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Document Map"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Plain Text"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="E-mail Signature"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="HTML Top of Form"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="HTML Bottom of Form"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Normal (Web)"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="HTML Acronym"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="HTML Address"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="HTML Cite"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="HTML Code"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="HTML Definition"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="HTML Keyboard"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="HTML Preformatted"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="HTML Sample"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="HTML Typewriter"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="HTML Variable"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Normal Table"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="annotation subject"/>
  <w:LsdException Locked="false" Priority="99" SemiHidden="true"
   UnhideWhenUsed="true" Name="No List"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Outline List 1"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Outline List 2"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Outline List 3"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Simple 1"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Simple 2"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Simple 3"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Classic 1"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Classic 2"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Classic 3"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Classic 4"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Colorful 1"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Colorful 2"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Colorful 3"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Columns 1"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Columns 2"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Columns 3"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Columns 4"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Columns 5"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Grid 1"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Grid 2"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Grid 3"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Grid 4"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Grid 5"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Grid 6"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Grid 7"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Grid 8"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table List 1"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table List 2"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table List 3"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table List 4"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table List 5"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table List 6"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table List 7"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table List 8"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table 3D effects 1"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table 3D effects 2"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table 3D effects 3"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Contemporary"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Elegant"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Professional"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Subtle 1"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Subtle 2"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Web 1"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Web 2"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Web 3"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Balloon Text"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Table Theme"/>
  <w:LsdException Locked="false" SemiHidden="true" Name="Placeholder Text"/>
  <w:LsdException Locked="false" SemiHidden="true" Name="Revision"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="Bibliography"/>
  <w:LsdException Locked="false" SemiHidden="true" UnhideWhenUsed="true"
   Name="TOC Heading"/>
  <w:LsdException Locked="false" Priority="49" Name="Grid Table 4"/>
  <w:LsdException Locked="false" Priority="50" Name="Grid Table 5 Dark"/>
  <w:LsdException Locked="false" Priority="51" Name="Grid Table 6 Colorful"/>
  <w:LsdException Locked="false" Priority="52" Name="Grid Table 7 Colorful"/>
  <w:LsdException Locked="false" Priority="46"
   Name="Grid Table 1 Light Accent 1"/>
  <w:LsdException Locked="false" Priority="47" Name="Grid Table 2 Accent 1"/>
  <w:LsdException Locked="false" Priority="48" Name="Grid Table 3 Accent 1"/>
  <w:LsdException Locked="false" Priority="49" Name="Grid Table 4 Accent 1"/>
  <w:LsdException Locked="false" Priority="50" Name="Grid Table 5 Dark Accent 1"/>
  <w:LsdException Locked="false" Priority="51"
   Name="Grid Table 6 Colorful Accent 1"/>
  <w:LsdException Locked="false" Priority="52"
   Name="Grid Table 7 Colorful Accent 1"/>
  <w:LsdException Locked="false" Priority="46"
   Name="Grid Table 1 Light Accent 2"/>
  <w:LsdException Locked="false" Priority="47" Name="Grid Table 2 Accent 2"/>
  <w:LsdException Locked="false" Priority="48" Name="Grid Table 3 Accent 2"/>
  <w:LsdException Locked="false" Priority="49" Name="Grid Table 4 Accent 2"/>
  <w:LsdException Locked="false" Priority="50" Name="Grid Table 5 Dark Accent 2"/>
  <w:LsdException Locked="false" Priority="51"
   Name="Grid Table 6 Colorful Accent 2"/>
  <w:LsdException Locked="false" Priority="52"
   Name="Grid Table 7 Colorful Accent 2"/>
  <w:LsdException Locked="false" Priority="46"
   Name="Grid Table 1 Light Accent 3"/>
  <w:LsdException Locked="false" Priority="47" Name="Grid Table 2 Accent 3"/>
  <w:LsdException Locked="false" Priority="48" Name="Grid Table 3 Accent 3"/>
  <w:LsdException Locked="false" Priority="49" Name="Grid Table 4 Accent 3"/>
  <w:LsdException Locked="false" Priority="50" Name="Grid Table 5 Dark Accent 3"/>
  <w:LsdException Locked="false" Priority="51"
   Name="Grid Table 6 Colorful Accent 3"/>
  <w:LsdException Locked="false" Priority="52"
   Name="Grid Table 7 Colorful Accent 3"/>
  <w:LsdException Locked="false" Priority="46"
   Name="Grid Table 1 Light Accent 4"/>
  <w:LsdException Locked="false" Priority="47" Name="Grid Table 2 Accent 4"/>
  <w:LsdException Locked="false" Priority="48" Name="Grid Table 3 Accent 4"/>
  <w:LsdException Locked="false" Priority="49" Name="Grid Table 4 Accent 4"/>
  <w:LsdException Locked="false" Priority="50" Name="Grid Table 5 Dark Accent 4"/>
  <w:LsdException Locked="false" Priority="51"
   Name="Grid Table 6 Colorful Accent 4"/>
  <w:LsdException Locked="false" Priority="52"
   Name="Grid Table 7 Colorful Accent 4"/>
  <w:LsdException Locked="false" Priority="46"
   Name="Grid Table 1 Light Accent 5"/>
  <w:LsdException Locked="false" Priority="47" Name="Grid Table 2 Accent 5"/>
  <w:LsdException Locked="false" Priority="48" Name="Grid Table 3 Accent 5"/>
  <w:LsdException Locked="false" Priority="49" Name="Grid Table 4 Accent 5"/>
  <w:LsdException Locked="false" Priority="50" Name="Grid Table 5 Dark Accent 5"/>
  <w:LsdException Locked="false" Priority="51"
   Name="Grid Table 6 Colorful Accent 5"/>
  <w:LsdException Locked="false" Priority="52"
   Name="Grid Table 7 Colorful Accent 5"/>
  <w:LsdException Locked="false" Priority="46"
   Name="Grid Table 1 Light Accent 6"/>
  <w:LsdException Locked="false" Priority="47" Name="Grid Table 2 Accent 6"/>
  <w:LsdException Locked="false" Priority="48" Name="Grid Table 3 Accent 6"/>
  <w:LsdException Locked="false" Priority="49" Name="Grid Table 4 Accent 6"/>
  <w:LsdException Locked="false" Priority="50" Name="Grid Table 5 Dark Accent 6"/>
  <w:LsdException Locked="false" Priority="51"
   Name="Grid Table 6 Colorful Accent 6"/>
  <w:LsdException Locked="false" Priority="52"
   Name="Grid Table 7 Colorful Accent 6"/>
  <w:LsdException Locked="false" Priority="46" Name="List Table 1 Light"/>
  <w:LsdException Locked="false" Priority="47" Name="List Table 2"/>
  <w:LsdException Locked="false" Priority="48" Name="List Table 3"/>
  <w:LsdException Locked="false" Priority="49" Name="List Table 4"/>
  <w:LsdException Locked="false" Priority="50" Name="List Table 5 Dark"/>
  <w:LsdException Locked="false" Priority="51" Name="List Table 6 Colorful"/>
  <w:LsdException Locked="false" Priority="52" Name="List Table 7 Colorful"/>
  <w:LsdException Locked="false" Priority="46"
   Name="List Table 1 Light Accent 1"/>
  <w:LsdException Locked="false" Priority="47" Name="List Table 2 Accent 1"/>
  <w:LsdException Locked="false" Priority="48" Name="List Table 3 Accent 1"/>
  <w:LsdException Locked="false" Priority="49" Name="List Table 4 Accent 1"/>
  <w:LsdException Locked="false" Priority="50" Name="List Table 5 Dark Accent 1"/>
  <w:LsdException Locked="false" Priority="51"
   Name="List Table 6 Colorful Accent 1"/>
  <w:LsdException Locked="false" Priority="52"
   Name="List Table 7 Colorful Accent 1"/>
  <w:LsdException Locked="false" Priority="46"
   Name="List Table 1 Light Accent 2"/>
  <w:LsdException Locked="false" Priority="47" Name="List Table 2 Accent 2"/>
  <w:LsdException Locked="false" Priority="48" Name="List Table 3 Accent 2"/>
  <w:LsdException Locked="false" Priority="49" Name="List Table 4 Accent 2"/>
  <w:LsdException Locked="false" Priority="50" Name="List Table 5 Dark Accent 2"/>
  <w:LsdException Locked="false" Priority="51"
   Name="List Table 6 Colorful Accent 2"/>
  <w:LsdException Locked="false" Priority="52"
   Name="List Table 7 Colorful Accent 2"/>
  <w:LsdException Locked="false" Priority="46"
   Name="List Table 1 Light Accent 3"/>
  <w:LsdException Locked="false" Priority="47" Name="List Table 2 Accent 3"/>
  <w:LsdException Locked="false" Priority="48" Name="List Table 3 Accent 3"/>
  <w:LsdException Locked="false" Priority="49" Name="List Table 4 Accent 3"/>
  <w:LsdException Locked="false" Priority="50" Name="List Table 5 Dark Accent 3"/>
  <w:LsdException Locked="false" Priority="51"
   Name="List Table 6 Colorful Accent 3"/>
  <w:LsdException Locked="false" Priority="52"
   Name="List Table 7 Colorful Accent 3"/>
  <w:LsdException Locked="false" Priority="46"
   Name="List Table 1 Light Accent 4"/>
  <w:LsdException Locked="false" Priority="47" Name="List Table 2 Accent 4"/>
  <w:LsdException Locked="false" Priority="48" Name="List Table 3 Accent 4"/>
  <w:LsdException Locked="false" Priority="49" Name="List Table 4 Accent 4"/>
  <w:LsdException Locked="false" Priority="50" Name="List Table 5 Dark Accent 4"/>
  <w:LsdException Locked="false" Priority="51"
   Name="List Table 6 Colorful Accent 4"/>
  <w:LsdException Locked="false" Priority="52"
   Name="List Table 7 Colorful Accent 4"/>
  <w:LsdException Locked="false" Priority="46"
   Name="List Table 1 Light Accent 5"/>
  <w:LsdException Locked="false" Priority="47" Name="List Table 2 Accent 5"/>
  <w:LsdException Locked="false" Priority="48" Name="List Table 3 Accent 5"/>
  <w:LsdException Locked="false" Priority="49" Name="List Table 4 Accent 5"/>
  <w:LsdException Locked="false" Priority="50" Name="List Table 5 Dark Accent 5"/>
  <w:LsdException Locked="false" Priority="51"
   Name="List Table 6 Colorful Accent 5"/>
  <w:LsdException Locked="false" Priority="52"
   Name="List Table 7 Colorful Accent 5"/>
  <w:LsdException Locked="false" Priority="46"
   Name="List Table 1 Light Accent 6"/>
  <w:LsdException Locked="false" Priority="47" Name="List Table 2 Accent 6"/>
  <w:LsdException Locked="false" Priority="48" Name="List Table 3 Accent 6"/>
  <w:LsdException Locked="false" Priority="49" Name="List Table 4 Accent 6"/>
  <w:LsdException Locked="false" Priority="50" Name="List Table 5 Dark Accent 6"/>
  <w:LsdException Locked="false" Priority="51"
   Name="List Table 6 Colorful Accent 6"/>
  <w:LsdException Locked="false" Priority="52"
   Name="List Table 7 Colorful Accent 6"/>
  <w:LsdException Locked="false" Priority="99" SemiHidden="true"
   UnhideWhenUsed="true" Name="Mention"/>
  <w:LsdException Locked="false" Priority="99" SemiHidden="true"
   UnhideWhenUsed="true" Name="Smart Hyperlink"/>
  <w:LsdException Locked="false" Priority="99" SemiHidden="true"
   UnhideWhenUsed="true" Name="Hashtag"/>
  <w:LsdException Locked="false" Priority="99" SemiHidden="true"
   UnhideWhenUsed="true" Name="Unresolved Mention"/>
 </w:LatentStyles>
</xml><![endif]-->
<style>
<!--
 /* Font Definitions */
 @font-face
	{font-family:宋体;
	panose-1:2 1 6 0 3 1 1 1 1 1;
	mso-font-alt:SimSun;
	mso-font-charset:134;
	mso-generic-font-family:auto;
	mso-font-pitch:variable;
	mso-font-signature:3 680460288 22 0 262145 0;}
@font-face
	{font-family:"Cambria Math";
	panose-1:2 4 5 3 5 4 6 3 2 4;
	mso-font-charset:0;
	mso-generic-font-family:roman;
	mso-font-pitch:variable;
	mso-font-signature:3 0 0 0 1 0;}
@font-face
	{font-family:Calibri;
	panose-1:2 15 5 2 2 2 4 3 2 4;
	mso-font-charset:0;
	mso-generic-font-family:swiss;
	mso-font-pitch:variable;
	mso-font-signature:-469750017 -1073732485 9 0 511 0;}
@font-face
	{font-family:Cambria;
	panose-1:2 4 5 3 5 4 6 3 2 4;
	mso-font-charset:0;
	mso-generic-font-family:roman;
	mso-font-pitch:variable;
	mso-font-signature:-536869121 1107305727 33554432 0 415 0;}
@font-face
	{font-family:Consolas;
	panose-1:2 11 6 9 2 2 4 3 2 4;
	mso-font-charset:0;
	mso-generic-font-family:roman;
	mso-font-pitch:auto;
	mso-font-signature:0 0 0 0 0 0;}
@font-face
	{font-family:"\@宋体";
	panose-1:2 1 6 0 3 1 1 1 1 1;
	mso-font-charset:134;
	mso-generic-font-family:auto;
	mso-font-pitch:variable;
	mso-font-signature:3 680460288 22 0 262145 0;}
 /* Style Definitions */
 p.MsoNormal, li.MsoNormal, div.MsoNormal
	{mso-style-unhide:no;
	mso-style-qformat:yes;
	mso-style-parent:"";
	margin-top:0cm;
	margin-right:0cm;
	margin-bottom:10.0pt;
	margin-left:0cm;
	mso-pagination:widow-orphan;
	font-size:12.0pt;
	font-family:"Cambria",serif;
	mso-ascii-font-family:Cambria;
	mso-ascii-theme-font:minor-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:minor-fareast;
	mso-hansi-font-family:Cambria;
	mso-hansi-theme-font:minor-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:minor-bidi;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
h1
	{mso-style-priority:9;
	mso-style-unhide:no;
	mso-style-qformat:yes;
	mso-style-next:正文文本;
	margin-top:24.0pt;
	margin-right:0cm;
	margin-bottom:0cm;
	margin-left:0cm;
	margin-bottom:.0001pt;
	mso-pagination:widow-orphan lines-together;
	page-break-after:avoid;
	mso-outline-level:1;
	font-size:16.0pt;
	font-family:"Calibri",sans-serif;
	mso-ascii-font-family:Calibri;
	mso-ascii-theme-font:major-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:major-fareast;
	mso-hansi-font-family:Calibri;
	mso-hansi-theme-font:major-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:major-bidi;
	color:#4F81BD;
	mso-themecolor:accent1;
	mso-font-kerning:0pt;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
h2
	{mso-style-priority:9;
	mso-style-qformat:yes;
	mso-style-next:正文文本;
	margin-top:10.0pt;
	margin-right:0cm;
	margin-bottom:0cm;
	margin-left:0cm;
	margin-bottom:.0001pt;
	mso-pagination:widow-orphan lines-together;
	page-break-after:avoid;
	mso-outline-level:2;
	font-size:14.0pt;
	font-family:"Calibri",sans-serif;
	mso-ascii-font-family:Calibri;
	mso-ascii-theme-font:major-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:major-fareast;
	mso-hansi-font-family:Calibri;
	mso-hansi-theme-font:major-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:major-bidi;
	color:#4F81BD;
	mso-themecolor:accent1;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
h3
	{mso-style-priority:9;
	mso-style-qformat:yes;
	mso-style-next:正文文本;
	margin-top:10.0pt;
	margin-right:0cm;
	margin-bottom:0cm;
	margin-left:0cm;
	margin-bottom:.0001pt;
	mso-pagination:widow-orphan lines-together;
	page-break-after:avoid;
	mso-outline-level:3;
	font-size:12.0pt;
	font-family:"Calibri",sans-serif;
	mso-ascii-font-family:Calibri;
	mso-ascii-theme-font:major-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:major-fareast;
	mso-hansi-font-family:Calibri;
	mso-hansi-theme-font:major-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:major-bidi;
	color:#4F81BD;
	mso-themecolor:accent1;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
h4
	{mso-style-priority:9;
	mso-style-qformat:yes;
	mso-style-next:正文文本;
	margin-top:10.0pt;
	margin-right:0cm;
	margin-bottom:0cm;
	margin-left:0cm;
	margin-bottom:.0001pt;
	mso-pagination:widow-orphan lines-together;
	page-break-after:avoid;
	mso-outline-level:4;
	font-size:12.0pt;
	font-family:"Calibri",sans-serif;
	mso-ascii-font-family:Calibri;
	mso-ascii-theme-font:major-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:major-fareast;
	mso-hansi-font-family:Calibri;
	mso-hansi-theme-font:major-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:major-bidi;
	color:#4F81BD;
	mso-themecolor:accent1;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;
	font-weight:normal;
	mso-bidi-font-weight:bold;
	font-style:italic;
	mso-bidi-font-style:normal;}
h5
	{mso-style-priority:9;
	mso-style-qformat:yes;
	mso-style-next:正文文本;
	margin-top:10.0pt;
	margin-right:0cm;
	margin-bottom:0cm;
	margin-left:0cm;
	margin-bottom:.0001pt;
	mso-pagination:widow-orphan lines-together;
	page-break-after:avoid;
	mso-outline-level:5;
	font-size:12.0pt;
	font-family:"Calibri",sans-serif;
	mso-ascii-font-family:Calibri;
	mso-ascii-theme-font:major-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:major-fareast;
	mso-hansi-font-family:Calibri;
	mso-hansi-theme-font:major-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:major-bidi;
	color:#4F81BD;
	mso-themecolor:accent1;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;
	font-weight:normal;
	mso-bidi-font-style:italic;}
h6
	{mso-style-priority:9;
	mso-style-qformat:yes;
	mso-style-next:正文文本;
	margin-top:10.0pt;
	margin-right:0cm;
	margin-bottom:0cm;
	margin-left:0cm;
	margin-bottom:.0001pt;
	mso-pagination:widow-orphan lines-together;
	page-break-after:avoid;
	mso-outline-level:6;
	font-size:12.0pt;
	font-family:"Calibri",sans-serif;
	mso-ascii-font-family:Calibri;
	mso-ascii-theme-font:major-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:major-fareast;
	mso-hansi-font-family:Calibri;
	mso-hansi-theme-font:major-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:major-bidi;
	color:#4F81BD;
	mso-themecolor:accent1;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;
	font-weight:normal;}
p.MsoHeading7, li.MsoHeading7, div.MsoHeading7
	{mso-style-priority:9;
	mso-style-qformat:yes;
	mso-style-next:正文文本;
	margin-top:10.0pt;
	margin-right:0cm;
	margin-bottom:0cm;
	margin-left:0cm;
	margin-bottom:.0001pt;
	mso-pagination:widow-orphan lines-together;
	page-break-after:avoid;
	mso-outline-level:7;
	font-size:12.0pt;
	font-family:"Calibri",sans-serif;
	mso-ascii-font-family:Calibri;
	mso-ascii-theme-font:major-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:major-fareast;
	mso-hansi-font-family:Calibri;
	mso-hansi-theme-font:major-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:major-bidi;
	color:#4F81BD;
	mso-themecolor:accent1;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
p.MsoHeading8, li.MsoHeading8, div.MsoHeading8
	{mso-style-priority:9;
	mso-style-qformat:yes;
	mso-style-next:正文文本;
	margin-top:10.0pt;
	margin-right:0cm;
	margin-bottom:0cm;
	margin-left:0cm;
	margin-bottom:.0001pt;
	mso-pagination:widow-orphan lines-together;
	page-break-after:avoid;
	mso-outline-level:8;
	font-size:12.0pt;
	font-family:"Calibri",sans-serif;
	mso-ascii-font-family:Calibri;
	mso-ascii-theme-font:major-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:major-fareast;
	mso-hansi-font-family:Calibri;
	mso-hansi-theme-font:major-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:major-bidi;
	color:#4F81BD;
	mso-themecolor:accent1;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
p.MsoHeading9, li.MsoHeading9, div.MsoHeading9
	{mso-style-priority:9;
	mso-style-qformat:yes;
	mso-style-next:正文文本;
	margin-top:10.0pt;
	margin-right:0cm;
	margin-bottom:0cm;
	margin-left:0cm;
	margin-bottom:.0001pt;
	mso-pagination:widow-orphan lines-together;
	page-break-after:avoid;
	mso-outline-level:9;
	font-size:12.0pt;
	font-family:"Calibri",sans-serif;
	mso-ascii-font-family:Calibri;
	mso-ascii-theme-font:major-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:major-fareast;
	mso-hansi-font-family:Calibri;
	mso-hansi-theme-font:major-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:major-bidi;
	color:#4F81BD;
	mso-themecolor:accent1;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
p.MsoFootnoteText, li.MsoFootnoteText, div.MsoFootnoteText
	{mso-style-priority:9;
	mso-style-qformat:yes;
	margin-top:0cm;
	margin-right:0cm;
	margin-bottom:10.0pt;
	margin-left:0cm;
	mso-pagination:widow-orphan;
	font-size:12.0pt;
	font-family:"Cambria",serif;
	mso-ascii-font-family:Cambria;
	mso-ascii-theme-font:minor-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:minor-fareast;
	mso-hansi-font-family:Cambria;
	mso-hansi-theme-font:minor-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:minor-bidi;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
p.MsoCaption, li.MsoCaption, div.MsoCaption
	{mso-style-unhide:no;
	mso-style-link:"题注 字符";
	margin-top:0cm;
	margin-right:0cm;
	margin-bottom:6.0pt;
	margin-left:0cm;
	mso-pagination:widow-orphan;
	font-size:12.0pt;
	font-family:"Cambria",serif;
	mso-ascii-font-family:Cambria;
	mso-ascii-theme-font:minor-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:minor-fareast;
	mso-hansi-font-family:Cambria;
	mso-hansi-theme-font:minor-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:minor-bidi;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;
	font-style:italic;
	mso-bidi-font-style:normal;}
span.MsoFootnoteReference
	{mso-style-unhide:no;
	mso-style-parent:"题注 字符";
	vertical-align:super;}
p.MsoTitle, li.MsoTitle, div.MsoTitle
	{mso-style-unhide:no;
	mso-style-qformat:yes;
	mso-style-next:正文文本;
	margin-top:24.0pt;
	margin-right:0cm;
	margin-bottom:12.0pt;
	margin-left:0cm;
	text-align:center;
	mso-pagination:widow-orphan lines-together;
	page-break-after:avoid;
	font-size:18.0pt;
	font-family:"Calibri",sans-serif;
	mso-ascii-font-family:Calibri;
	mso-ascii-theme-font:major-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:major-fareast;
	mso-hansi-font-family:Calibri;
	mso-hansi-theme-font:major-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:major-bidi;
	color:#345A8A;
	mso-themecolor:accent1;
	mso-themeshade:181;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;
	font-weight:bold;}
p.MsoBodyText, li.MsoBodyText, div.MsoBodyText
	{mso-style-unhide:no;
	mso-style-qformat:yes;
	margin-top:9.0pt;
	margin-right:0cm;
	margin-bottom:9.0pt;
	margin-left:0cm;
	mso-pagination:widow-orphan;
	font-size:12.0pt;
	font-family:"Cambria",serif;
	mso-ascii-font-family:Cambria;
	mso-ascii-theme-font:minor-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:minor-fareast;
	mso-hansi-font-family:Cambria;
	mso-hansi-theme-font:minor-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:minor-bidi;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
p.MsoSubtitle, li.MsoSubtitle, div.MsoSubtitle
	{mso-style-unhide:no;
	mso-style-qformat:yes;
	mso-style-parent:标题;
	mso-style-next:正文文本;
	margin-top:12.0pt;
	margin-right:0cm;
	margin-bottom:12.0pt;
	margin-left:0cm;
	text-align:center;
	mso-pagination:widow-orphan lines-together;
	page-break-after:avoid;
	font-size:15.0pt;
	font-family:"Calibri",sans-serif;
	mso-ascii-font-family:Calibri;
	mso-ascii-theme-font:major-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:major-fareast;
	mso-hansi-font-family:Calibri;
	mso-hansi-theme-font:major-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:major-bidi;
	color:#345A8A;
	mso-themecolor:accent1;
	mso-themeshade:181;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;
	font-weight:bold;}
p.MsoDate, li.MsoDate, div.MsoDate
	{mso-style-unhide:no;
	mso-style-qformat:yes;
	mso-style-parent:"";
	mso-style-next:正文文本;
	margin-top:0cm;
	margin-right:0cm;
	margin-bottom:10.0pt;
	margin-left:0cm;
	text-align:center;
	mso-pagination:widow-orphan lines-together;
	page-break-after:avoid;
	font-size:12.0pt;
	font-family:"Cambria",serif;
	mso-ascii-font-family:Cambria;
	mso-ascii-theme-font:minor-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:minor-fareast;
	mso-hansi-font-family:Cambria;
	mso-hansi-theme-font:minor-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:minor-bidi;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
p.MsoBlockText, li.MsoBlockText, div.MsoBlockText
	{mso-style-priority:9;
	mso-style-qformat:yes;
	mso-style-parent:正文文本;
	mso-style-next:正文文本;
	margin-top:5.0pt;
	margin-right:24.0pt;
	margin-bottom:5.0pt;
	margin-left:24.0pt;
	mso-pagination:widow-orphan;
	font-size:12.0pt;
	font-family:"Cambria",serif;
	mso-ascii-font-family:Cambria;
	mso-ascii-theme-font:minor-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:minor-fareast;
	mso-hansi-font-family:Cambria;
	mso-hansi-theme-font:minor-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:minor-bidi;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
a:link, span.MsoHyperlink
	{mso-style-unhide:no;
	mso-style-parent:"题注 字符";
	color:#4F81BD;
	mso-themecolor:accent1;}
a:visited, span.MsoHyperlinkFollowed
	{mso-style-noshow:yes;
	color:purple;
	mso-themecolor:followedhyperlink;
	text-decoration:underline;
	text-underline:single;}
p.MsoBibliography, li.MsoBibliography, div.MsoBibliography
	{mso-style-unhide:no;
	mso-style-qformat:yes;
	margin-top:0cm;
	margin-right:0cm;
	margin-bottom:10.0pt;
	margin-left:0cm;
	mso-pagination:widow-orphan;
	font-size:12.0pt;
	font-family:"Cambria",serif;
	mso-ascii-font-family:Cambria;
	mso-ascii-theme-font:minor-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:minor-fareast;
	mso-hansi-font-family:Cambria;
	mso-hansi-theme-font:minor-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:minor-bidi;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
p.MsoTocHeading, li.MsoTocHeading, div.MsoTocHeading
	{mso-style-priority:39;
	mso-style-qformat:yes;
	mso-style-parent:"标题 1";
	mso-style-next:正文文本;
	margin-top:12.0pt;
	margin-right:0cm;
	margin-bottom:0cm;
	margin-left:0cm;
	margin-bottom:.0001pt;
	line-height:107%;
	mso-pagination:widow-orphan lines-together;
	page-break-after:avoid;
	font-size:16.0pt;
	font-family:"Calibri",sans-serif;
	mso-ascii-font-family:Calibri;
	mso-ascii-theme-font:major-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:major-fareast;
	mso-hansi-font-family:Calibri;
	mso-hansi-theme-font:major-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:major-bidi;
	color:#365F91;
	mso-themecolor:accent1;
	mso-themeshade:191;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
p.FirstParagraph, li.FirstParagraph, div.FirstParagraph
	{mso-style-name:"First Paragraph";
	mso-style-unhide:no;
	mso-style-qformat:yes;
	mso-style-parent:正文文本;
	mso-style-next:正文文本;
	margin-top:9.0pt;
	margin-right:0cm;
	margin-bottom:9.0pt;
	margin-left:0cm;
	mso-pagination:widow-orphan;
	font-size:12.0pt;
	font-family:"Cambria",serif;
	mso-ascii-font-family:Cambria;
	mso-ascii-theme-font:minor-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:minor-fareast;
	mso-hansi-font-family:Cambria;
	mso-hansi-theme-font:minor-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:minor-bidi;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
p.Compact, li.Compact, div.Compact
	{mso-style-name:Compact;
	mso-style-unhide:no;
	mso-style-qformat:yes;
	mso-style-parent:正文文本;
	margin-top:1.8pt;
	margin-right:0cm;
	margin-bottom:1.8pt;
	margin-left:0cm;
	mso-pagination:widow-orphan;
	font-size:12.0pt;
	font-family:"Cambria",serif;
	mso-ascii-font-family:Cambria;
	mso-ascii-theme-font:minor-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:minor-fareast;
	mso-hansi-font-family:Cambria;
	mso-hansi-theme-font:minor-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:minor-bidi;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
p.Author, li.Author, div.Author
	{mso-style-name:Author;
	mso-style-unhide:no;
	mso-style-qformat:yes;
	mso-style-parent:"";
	mso-style-next:正文文本;
	margin-top:0cm;
	margin-right:0cm;
	margin-bottom:10.0pt;
	margin-left:0cm;
	text-align:center;
	mso-pagination:widow-orphan lines-together;
	page-break-after:avoid;
	font-size:12.0pt;
	font-family:"Cambria",serif;
	mso-ascii-font-family:Cambria;
	mso-ascii-theme-font:minor-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:minor-fareast;
	mso-hansi-font-family:Cambria;
	mso-hansi-theme-font:minor-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:minor-bidi;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
p.Abstract, li.Abstract, div.Abstract
	{mso-style-name:Abstract;
	mso-style-unhide:no;
	mso-style-qformat:yes;
	mso-style-next:正文文本;
	margin-top:15.0pt;
	margin-right:0cm;
	margin-bottom:15.0pt;
	margin-left:0cm;
	mso-pagination:widow-orphan lines-together;
	page-break-after:avoid;
	font-size:10.0pt;
	font-family:"Cambria",serif;
	mso-ascii-font-family:Cambria;
	mso-ascii-theme-font:minor-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:minor-fareast;
	mso-hansi-font-family:Cambria;
	mso-hansi-theme-font:minor-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:minor-bidi;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
p.DefinitionTerm, li.DefinitionTerm, div.DefinitionTerm
	{mso-style-name:"Definition Term";
	mso-style-unhide:no;
	mso-style-next:Definition;
	margin:0cm;
	margin-bottom:.0001pt;
	mso-pagination:widow-orphan lines-together;
	page-break-after:avoid;
	font-size:12.0pt;
	font-family:"Cambria",serif;
	mso-ascii-font-family:Cambria;
	mso-ascii-theme-font:minor-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:minor-fareast;
	mso-hansi-font-family:Cambria;
	mso-hansi-theme-font:minor-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:minor-bidi;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;
	font-weight:bold;
	mso-bidi-font-weight:normal;}
p.Definition, li.Definition, div.Definition
	{mso-style-name:Definition;
	mso-style-unhide:no;
	margin-top:0cm;
	margin-right:0cm;
	margin-bottom:10.0pt;
	margin-left:0cm;
	mso-pagination:widow-orphan;
	font-size:12.0pt;
	font-family:"Cambria",serif;
	mso-ascii-font-family:Cambria;
	mso-ascii-theme-font:minor-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:minor-fareast;
	mso-hansi-font-family:Cambria;
	mso-hansi-theme-font:minor-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:minor-bidi;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
p.TableCaption, li.TableCaption, div.TableCaption
	{mso-style-name:"Table Caption";
	mso-style-unhide:no;
	mso-style-parent:题注;
	margin-top:0cm;
	margin-right:0cm;
	margin-bottom:6.0pt;
	margin-left:0cm;
	mso-pagination:widow-orphan;
	page-break-after:avoid;
	font-size:12.0pt;
	font-family:"Cambria",serif;
	mso-ascii-font-family:Cambria;
	mso-ascii-theme-font:minor-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:minor-fareast;
	mso-hansi-font-family:Cambria;
	mso-hansi-theme-font:minor-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:minor-bidi;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;
	font-style:italic;
	mso-bidi-font-style:normal;}
p.ImageCaption, li.ImageCaption, div.ImageCaption
	{mso-style-name:"Image Caption";
	mso-style-unhide:no;
	mso-style-parent:题注;
	margin-top:0cm;
	margin-right:0cm;
	margin-bottom:6.0pt;
	margin-left:0cm;
	mso-pagination:widow-orphan;
	font-size:12.0pt;
	font-family:"Cambria",serif;
	mso-ascii-font-family:Cambria;
	mso-ascii-theme-font:minor-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:minor-fareast;
	mso-hansi-font-family:Cambria;
	mso-hansi-theme-font:minor-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:minor-bidi;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;
	font-style:italic;
	mso-bidi-font-style:normal;}
p.Figure, li.Figure, div.Figure
	{mso-style-name:Figure;
	mso-style-unhide:no;
	margin-top:0cm;
	margin-right:0cm;
	margin-bottom:10.0pt;
	margin-left:0cm;
	mso-pagination:widow-orphan;
	font-size:12.0pt;
	font-family:"Cambria",serif;
	mso-ascii-font-family:Cambria;
	mso-ascii-theme-font:minor-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:minor-fareast;
	mso-hansi-font-family:Cambria;
	mso-hansi-theme-font:minor-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:minor-bidi;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
p.CaptionedFigure, li.CaptionedFigure, div.CaptionedFigure
	{mso-style-name:"Captioned Figure";
	mso-style-unhide:no;
	mso-style-parent:Figure;
	margin-top:0cm;
	margin-right:0cm;
	margin-bottom:10.0pt;
	margin-left:0cm;
	mso-pagination:widow-orphan;
	page-break-after:avoid;
	font-size:12.0pt;
	font-family:"Cambria",serif;
	mso-ascii-font-family:Cambria;
	mso-ascii-theme-font:minor-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:minor-fareast;
	mso-hansi-font-family:Cambria;
	mso-hansi-theme-font:minor-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:minor-bidi;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
span.a
	{mso-style-name:"题注 字符";
	mso-style-unhide:no;
	mso-style-locked:yes;
	mso-style-link:题注;}
span.VerbatimChar
	{mso-style-name:"Verbatim Char";
	mso-style-unhide:no;
	mso-style-locked:yes;
	mso-style-parent:"题注 字符";
	mso-style-link:"Source Code";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;}
span.SectionNumber
	{mso-style-name:"Section Number";
	mso-style-unhide:no;
	mso-style-parent:"题注 字符";}
p.SourceCode, li.SourceCode, div.SourceCode
	{mso-style-name:"Source Code";
	mso-style-unhide:no;
	mso-style-link:"Verbatim Char";
	margin-top:0cm;
	margin-right:0cm;
	margin-bottom:10.0pt;
	margin-left:0cm;
	mso-pagination:widow-orphan;
	word-break:break-all;
	font-size:12.0pt;
	font-family:"Cambria",serif;
	mso-ascii-font-family:Cambria;
	mso-ascii-theme-font:minor-latin;
	mso-fareast-font-family:宋体;
	mso-fareast-theme-font:minor-fareast;
	mso-hansi-font-family:Cambria;
	mso-hansi-theme-font:minor-latin;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:minor-bidi;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
span.KeywordTok
	{mso-style-name:KeywordTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#007020;
	font-weight:bold;
	mso-bidi-font-weight:normal;}
span.DataTypeTok
	{mso-style-name:DataTypeTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#902000;}
span.DecValTok
	{mso-style-name:DecValTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#40A070;}
span.BaseNTok
	{mso-style-name:BaseNTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#40A070;}
span.FloatTok
	{mso-style-name:FloatTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#40A070;}
span.ConstantTok
	{mso-style-name:ConstantTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#880000;}
span.CharTok
	{mso-style-name:CharTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#4070A0;}
span.SpecialCharTok
	{mso-style-name:SpecialCharTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#4070A0;}
span.StringTok
	{mso-style-name:StringTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#4070A0;}
span.VerbatimStringTok
	{mso-style-name:VerbatimStringTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#4070A0;}
span.SpecialStringTok
	{mso-style-name:SpecialStringTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#BB6688;}
span.ImportTok
	{mso-style-name:ImportTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;}
span.CommentTok
	{mso-style-name:CommentTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#60A0B0;
	font-style:italic;
	mso-bidi-font-style:normal;}
span.DocumentationTok
	{mso-style-name:DocumentationTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#BA2121;
	font-style:italic;
	mso-bidi-font-style:normal;}
span.AnnotationTok
	{mso-style-name:AnnotationTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#60A0B0;
	font-weight:bold;
	mso-bidi-font-weight:normal;
	font-style:italic;
	mso-bidi-font-style:normal;}
span.CommentVarTok
	{mso-style-name:CommentVarTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#60A0B0;
	font-weight:bold;
	mso-bidi-font-weight:normal;
	font-style:italic;
	mso-bidi-font-style:normal;}
span.OtherTok
	{mso-style-name:OtherTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#007020;}
span.FunctionTok
	{mso-style-name:FunctionTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#06287E;}
span.VariableTok
	{mso-style-name:VariableTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#19177C;}
span.ControlFlowTok
	{mso-style-name:ControlFlowTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#007020;
	font-weight:bold;
	mso-bidi-font-weight:normal;}
span.OperatorTok
	{mso-style-name:OperatorTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#666666;}
span.BuiltInTok
	{mso-style-name:BuiltInTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;}
span.ExtensionTok
	{mso-style-name:ExtensionTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;}
span.PreprocessorTok
	{mso-style-name:PreprocessorTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#BC7A00;}
span.AttributeTok
	{mso-style-name:AttributeTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#7D9029;}
span.RegionMarkerTok
	{mso-style-name:RegionMarkerTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;}
span.InformationTok
	{mso-style-name:InformationTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#60A0B0;
	font-weight:bold;
	mso-bidi-font-weight:normal;
	font-style:italic;
	mso-bidi-font-style:normal;}
span.WarningTok
	{mso-style-name:WarningTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:#60A0B0;
	font-weight:bold;
	mso-bidi-font-weight:normal;
	font-style:italic;
	mso-bidi-font-style:normal;}
span.AlertTok
	{mso-style-name:AlertTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:red;
	font-weight:bold;
	mso-bidi-font-weight:normal;}
span.ErrorTok
	{mso-style-name:ErrorTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;
	color:red;
	font-weight:bold;
	mso-bidi-font-weight:normal;}
span.NormalTok
	{mso-style-name:NormalTok;
	mso-style-unhide:no;
	mso-style-parent:"Verbatim Char";
	mso-ansi-font-size:11.0pt;
	font-family:"Consolas",serif;
	mso-ascii-font-family:Consolas;
	mso-hansi-font-family:Consolas;}
span.GramE
	{mso-style-name:"";
	mso-gram-e:yes;}
.MsoChpDefault
	{mso-style-type:export-only;
	mso-default-props:yes;
	font-size:12.0pt;
	mso-ansi-font-size:12.0pt;
	mso-bidi-font-size:12.0pt;
	font-family:"Cambria",serif;
	mso-bidi-font-family:"Times New Roman";
	mso-bidi-theme-font:minor-bidi;
	mso-font-kerning:0pt;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
.MsoPapDefault
	{mso-style-type:export-only;
	margin-bottom:10.0pt;}
 /* Page Definitions */
 @page
	{mso-page-border-surround-header:no;
	mso-page-border-surround-footer:no;
	mso-footnote-separator:url("12.files/header.htm") fs;
	mso-footnote-continuation-separator:url("12.files/header.htm") fcs;
	mso-endnote-separator:url("12.files/header.htm") es;
	mso-endnote-continuation-separator:url("12.files/header.htm") ecs;}
@page WordSection1
	{size:612.0pt 792.0pt;
	margin:72.0pt 90.0pt 72.0pt 90.0pt;
	mso-header-margin:36.0pt;
	mso-footer-margin:36.0pt;
	mso-paper-source:0;}
div.WordSection1
	{page:WordSection1;}
 /* List Definitions */
 @list l0
	{mso-list-id:739959809;
	mso-list-template-ids:40945652;}
@list l0:level1
	{mso-level-start-at:0;
	mso-level-number-format:bullet;
	mso-level-text:" ";
	mso-level-tab-stop:none;
	mso-level-number-position:left;
	text-indent:-24.0pt;}
@list l0:level2
	{mso-level-start-at:0;
	mso-level-number-format:bullet;
	mso-level-text:" ";
	mso-level-tab-stop:none;
	mso-level-number-position:left;
	text-indent:-24.0pt;}
@list l0:level3
	{mso-level-start-at:0;
	mso-level-number-format:bullet;
	mso-level-text:" ";
	mso-level-tab-stop:none;
	mso-level-number-position:left;
	text-indent:-24.0pt;}
@list l0:level4
	{mso-level-start-at:0;
	mso-level-number-format:bullet;
	mso-level-text:" ";
	mso-level-tab-stop:none;
	mso-level-number-position:left;
	text-indent:-24.0pt;}
@list l0:level5
	{mso-level-start-at:0;
	mso-level-number-format:bullet;
	mso-level-text:" ";
	mso-level-tab-stop:none;
	mso-level-number-position:left;
	text-indent:-24.0pt;}
@list l0:level6
	{mso-level-start-at:0;
	mso-level-number-format:bullet;
	mso-level-text:" ";
	mso-level-tab-stop:none;
	mso-level-number-position:left;
	text-indent:-24.0pt;}
@list l0:level7
	{mso-level-start-at:0;
	mso-level-number-format:bullet;
	mso-level-text:" ";
	mso-level-tab-stop:none;
	mso-level-number-position:left;
	text-indent:-24.0pt;}
@list l0:level8
	{mso-level-start-at:0;
	mso-level-number-format:bullet;
	mso-level-text:" ";
	mso-level-tab-stop:none;
	mso-level-number-position:left;
	text-indent:-24.0pt;}
@list l0:level9
	{mso-level-start-at:0;
	mso-level-number-format:bullet;
	mso-level-text:" ";
	mso-level-tab-stop:none;
	mso-level-number-position:left;
	text-indent:-24.0pt;}
ol
	{margin-bottom:0cm;}
ul
	{margin-bottom:0cm;}
-->
</style>
<!--[if gte mso 10]>
<style>
 /* Style Definitions */
 table.MsoNormalTable
	{mso-style-name:普通表格;
	mso-tstyle-rowband-size:0;
	mso-tstyle-colband-size:0;
	mso-style-noshow:yes;
	mso-style-priority:99;
	mso-style-parent:"";
	mso-padding-alt:0cm 5.4pt 0cm 5.4pt;
	mso-para-margin-top:0cm;
	mso-para-margin-right:0cm;
	mso-para-margin-bottom:10.0pt;
	mso-para-margin-left:0cm;
	mso-pagination:widow-orphan;
	font-size:12.0pt;
	font-family:"Cambria",serif;
	mso-ascii-font-family:Cambria;
	mso-ascii-theme-font:minor-latin;
	mso-hansi-font-family:Cambria;
	mso-hansi-theme-font:minor-latin;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
table.Table
	{mso-style-name:Table;
	mso-tstyle-rowband-size:0;
	mso-tstyle-colband-size:0;
	mso-style-noshow:yes;
	mso-style-qformat:yes;
	mso-style-parent:"";
	mso-padding-alt:0cm 5.4pt 0cm 5.4pt;
	mso-para-margin-top:0cm;
	mso-para-margin-right:0cm;
	mso-para-margin-bottom:10.0pt;
	mso-para-margin-left:0cm;
	mso-pagination:widow-orphan;
	font-size:12.0pt;
	font-family:"Cambria",serif;
	mso-ascii-font-family:Cambria;
	mso-ascii-theme-font:minor-latin;
	mso-hansi-font-family:Cambria;
	mso-hansi-theme-font:minor-latin;
	mso-ansi-language:EN;
	mso-fareast-language:EN-US;}
table.TableFirstRow
	{mso-style-name:Table;
	mso-table-condition:first-row;
	mso-style-noshow:yes;
	mso-style-qformat:yes;
	mso-style-parent:"";
	mso-tstyle-vert-align:bottom;
	mso-tstyle-border-bottom:.25pt solid windowtext;}
</style>
<![endif]--><!--[if gte mso 9]><xml>
 <o:shapedefaults v:ext="edit" spidmax="1026"/>
</xml><![endif]--><!--[if gte mso 9]><xml>
 <o:shapelayout v:ext="edit">
  <o:idmap v:ext="edit" data="1"/>
 </o:shapelayout></xml><![endif]-->
</head>

<body lang=ZH-CN link="#4F81BD" vlink=purple style='tab-interval:36.0pt'>

<div class=WordSection1>

<h1><span style='font-family:宋体;mso-ascii-font-family:Calibri;mso-ascii-theme-font:
major-latin;mso-fareast-theme-font:major-fareast;mso-hansi-font-family:Calibri;
mso-hansi-theme-font:major-latin;mso-fareast-language:ZH-CN'>一、开展商品期货套期保值业务的目的</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></h1>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>天海融合防务装备技术股份有限公司（以下简称</span><span lang=EN style='mso-fareast-language:
ZH-CN'>“</span><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>公司</span><span lang=EN style='mso-fareast-language:ZH-CN'>”</span><span
style='font-family:宋体;mso-ascii-font-family:Cambria;mso-ascii-theme-font:minor-latin;
mso-fareast-theme-font:minor-fareast;mso-hansi-font-family:Cambria;mso-hansi-theme-font:
minor-latin;mso-fareast-language:ZH-CN'>或</span><span lang=EN style='mso-fareast-language:
ZH-CN'>“</span><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>天海防务</span><span lang=EN style='mso-fareast-language:ZH-CN'>”</span><span
style='font-family:宋体;mso-ascii-font-family:Cambria;mso-ascii-theme-font:minor-latin;
mso-fareast-theme-font:minor-fareast;mso-hansi-font-family:Cambria;mso-hansi-theme-font:
minor-latin;mso-fareast-language:ZH-CN'>）主要从事船舶与海洋工程业务涵盖船海工程研发设计、工程咨询和工程监理、总装集成制造等，形成了全方位、多层次的技术服务体系，各业务间既相互独立经营，又协同发展，实现了良性的互动效应。</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>在生产经营过程中，公司全资子公司江苏大津重工有限公司（以下简称</span><span lang=EN style='mso-fareast-language:
ZH-CN'>“</span><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>大津重工</span><span lang=EN style='mso-fareast-language:ZH-CN'>”</span><span
style='font-family:宋体;mso-ascii-font-family:Cambria;mso-ascii-theme-font:minor-latin;
mso-fareast-theme-font:minor-fareast;mso-hansi-font-family:Cambria;mso-hansi-theme-font:
minor-latin;mso-fareast-language:ZH-CN'>）需采购大量钢板作为原材料，但受需求<span class=GramE>端持续</span>回暖及供给端减产影响，今年以来国内钢板价格持续上涨。公司新能源业务自</span><span
lang=EN style='mso-fareast-language:ZH-CN'>2021</span><span style='font-family:
宋体;mso-ascii-font-family:Cambria;mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:
minor-fareast;mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;
mso-fareast-language:ZH-CN'>年</span><span lang=EN style='mso-fareast-language:
ZH-CN'>4</span><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>月以来开展了焦炭贸易业务。</span><span lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>为加强<span class=GramE>大津重工</span>生产经营的成本管理，为了有效防范新能源业务经营活动中焦炭价格波动的风险，保证订单成本的相对稳定，降低价格波动公司正常经营的影响，公司及下属子公司拟使用自有资金，开展包括钢材、焦炭等商品的期货套期保值业务，充分利用期货市场的套期保值功能，降低原材料市场价格波动对公司生产经营成本的影响，有效控制市场风险，不以逐利为目的进行投机交易，有利于提升公司整体抵御风险的能力，增强财务稳健性。</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<h1><span style='font-family:宋体;mso-ascii-font-family:Calibri;mso-ascii-theme-font:
major-latin;mso-fareast-theme-font:major-fareast;mso-hansi-font-family:Calibri;
mso-hansi-theme-font:major-latin;mso-fareast-language:ZH-CN'>二、开展商品期货套期保值业务基本情况</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></h1>

<h2><span style='font-family:宋体;mso-ascii-font-family:Calibri;mso-ascii-theme-font:
major-latin;mso-fareast-theme-font:major-fareast;mso-hansi-font-family:Calibri;
mso-hansi-theme-font:major-latin;mso-fareast-language:ZH-CN'>（一）期货套期保值交易品种</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></h2>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>公司及下属子公司拟申请开展的期货套期保值业务将只限于在境内期货交易所交易的钢材及焦炭期货品种，严禁进行以盈利为目的的任何投机交易。</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<h2><span style='font-family:宋体;mso-ascii-font-family:Calibri;mso-ascii-theme-font:
major-latin;mso-fareast-theme-font:major-fareast;mso-hansi-font-family:Calibri;
mso-hansi-theme-font:major-latin;mso-fareast-language:ZH-CN'>（二）投资期限</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></h2>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>拟自本次董事会审议通过之日起至</span><span lang=EN style='mso-fareast-language:ZH-CN'>2021</span><span
style='font-family:宋体;mso-ascii-font-family:Cambria;mso-ascii-theme-font:minor-latin;
mso-fareast-theme-font:minor-fareast;mso-hansi-font-family:Cambria;mso-hansi-theme-font:
minor-latin;mso-fareast-language:ZH-CN'>年年度董事会召开前有效。</span><span lang=EN
style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<h2><span style='font-family:宋体;mso-ascii-font-family:Calibri;mso-ascii-theme-font:
major-latin;mso-fareast-theme-font:major-fareast;mso-hansi-font-family:Calibri;
mso-hansi-theme-font:major-latin;mso-fareast-language:ZH-CN'>（三）预计交易数量、投入金额</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></h2>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>公司及下属子公司将根据实际情况，开展钢材期货套期保值业务，对合计不超过</span><span lang=EN
style='mso-fareast-language:ZH-CN'>8,000 </span><span style='font-family:宋体;
mso-ascii-font-family:Cambria;mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:
minor-fareast;mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;
mso-fareast-language:ZH-CN'>吨钢材期货套期保值，总计投入保证金不超过（即授权有效期内任一</span><span lang=EN
style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>时点都不超过）</span><span lang=EN style='mso-fareast-language:ZH-CN'>800</span><span
style='font-family:宋体;mso-ascii-font-family:Cambria;mso-ascii-theme-font:minor-latin;
mso-fareast-theme-font:minor-fareast;mso-hansi-font-family:Cambria;mso-hansi-theme-font:
minor-latin;mso-fareast-language:ZH-CN'>万元，在上述额度范围内，资金可循环使用；对合计不超过</span><span
lang=EN style='mso-fareast-language:ZH-CN'>5,000 </span><span style='font-family:
宋体;mso-ascii-font-family:Cambria;mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:
minor-fareast;mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;
mso-fareast-language:ZH-CN'>吨焦炭期货套期保值，总计投入保证金不超过（即授权有效期内任一时点都不超过）</span><span
lang=EN style='mso-fareast-language:ZH-CN'>800</span><span style='font-family:
宋体;mso-ascii-font-family:Cambria;mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:
minor-fareast;mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;
mso-fareast-language:ZH-CN'>万元，在上述额度范围内，资金可循环使用。</span><span lang=EN
style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>期货套期保值操作小组将根据市场情况分批投入保证金，不会对公司及下属子公司的经营资金产生较大影响。</span><span lang=EN
style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<h2><span style='font-family:宋体;mso-ascii-font-family:Calibri;mso-ascii-theme-font:
major-latin;mso-fareast-theme-font:major-fareast;mso-hansi-font-family:Calibri;
mso-hansi-theme-font:major-latin;mso-fareast-language:ZH-CN'>（四）资金来源</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></h2>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>自有资金。</span><span lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<h1><span style='font-family:宋体;mso-ascii-font-family:Calibri;mso-ascii-theme-font:
major-latin;mso-fareast-theme-font:major-fareast;mso-hansi-font-family:Calibri;
mso-hansi-theme-font:major-latin;mso-fareast-language:ZH-CN'>三、开展商品期货套期保值业务的可行性分析</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></h1>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>今年以来，铁矿石、铜、铝等大宗商品价格快速上涨，国内</span><span lang=EN style='mso-fareast-language:
ZH-CN'>6mm</span><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>造船板和</span><span lang=EN style='mso-fareast-language:ZH-CN'>20mm</span><span
style='font-family:宋体;mso-ascii-font-family:Cambria;mso-ascii-theme-font:minor-latin;
mso-fareast-theme-font:minor-fareast;mso-hansi-font-family:Cambria;mso-hansi-theme-font:
minor-latin;mso-fareast-language:ZH-CN'>造船板价格一度达到</span><span lang=EN
style='mso-fareast-language:ZH-CN'>7590</span><span style='font-family:宋体;
mso-ascii-font-family:Cambria;mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:
minor-fareast;mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;
mso-fareast-language:ZH-CN'>元</span><span lang=EN style='mso-fareast-language:
ZH-CN'>/</span><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>吨和</span><span lang=EN style='mso-fareast-language:ZH-CN'>7120</span><span
style='font-family:宋体;mso-ascii-font-family:Cambria;mso-ascii-theme-font:minor-latin;
mso-fareast-theme-font:minor-fareast;mso-hansi-font-family:Cambria;mso-hansi-theme-font:
minor-latin;mso-fareast-language:ZH-CN'>元</span><span lang=EN style='mso-fareast-language:
ZH-CN'>/</span><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>吨，同比上涨</span><span lang=EN style='mso-fareast-language:ZH-CN'>70.9%</span><span
style='font-family:宋体;mso-ascii-font-family:Cambria;mso-ascii-theme-font:minor-latin;
mso-fareast-theme-font:minor-fareast;mso-hansi-font-family:Cambria;mso-hansi-theme-font:
minor-latin;mso-fareast-language:ZH-CN'>和</span><span lang=EN style='mso-fareast-language:
ZH-CN'>79.3%</span><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>。尽管近期钢材价格有所回落，但仍保持在</span><span lang=EN style='mso-fareast-language:
ZH-CN'>6000</span><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>元</span><span lang=EN style='mso-fareast-language:ZH-CN'>/</span><span
style='font-family:宋体;mso-ascii-font-family:Cambria;mso-ascii-theme-font:minor-latin;
mso-fareast-theme-font:minor-fareast;mso-hansi-font-family:Cambria;mso-hansi-theme-font:
minor-latin;mso-fareast-language:ZH-CN'>吨以上的高位，广大造船企业承受着巨大成本压力。以钢材为重要原材料的<span
class=GramE>大津重工</span>如能适时开展钢材的套期保值业务，可有效减少钢板价格波动所带来的成本压力，有利于锁定预期利润、减少价格波动造成的损失，具有较强的可行性和必要性。</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>与此同时，公司全资子公司上海佳豪沃金新能源有限公司（以下简称</span><span lang=EN style='mso-fareast-language:
ZH-CN'>“</span><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>沃金新能源</span><span lang=EN style='mso-fareast-language:ZH-CN'>”</span><span
style='font-family:宋体;mso-ascii-font-family:Cambria;mso-ascii-theme-font:minor-latin;
mso-fareast-theme-font:minor-fareast;mso-hansi-font-family:Cambria;mso-hansi-theme-font:
minor-latin;mso-fareast-language:ZH-CN'>）根据经营需需求，于</span><span lang=EN
style='mso-fareast-language:ZH-CN'>2021</span><span style='font-family:宋体;
mso-ascii-font-family:Cambria;mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:
minor-fareast;mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;
mso-fareast-language:ZH-CN'>年</span><span lang=EN style='mso-fareast-language:
ZH-CN'>4</span><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>月以来开展了焦炭贸易业务，受国际形势动荡影响，大宗商品价格出现大幅波动，焦炭也波及其中，如沃金新能源合理利用期货工具，可有效减少焦炭价格波动带来的经营风险，有利于锁定预期利润和减少价格波动造成的损失，符合沃金新能源日常经营需要，存在可行性和必要性。</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>公司董事会制定了《期货套期保值业务管理制度》，对期货套期保值业务的审批权限及信息披露、内部操作流程、风险管理及处理程序等做出明确规定，能够有效保障期货业务的顺利进行，并对风险形成有效控制。</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>公司将成立期货套期保值领导小组，负责公司期货套期保值业务相关事宜。相关业务部门及子公司将成立具体期货套期保值操作小组，组织具有良好素质的专门人员负责期货业务的交易工作。</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>公司及下属子公司具备与期货套期保值业务的交易保证金相匹配的自有资金。</span><span lang=EN style='mso-fareast-language:
ZH-CN'><o:p></o:p></span></p>

<h1><span style='font-family:宋体;mso-ascii-font-family:Calibri;mso-ascii-theme-font:
major-latin;mso-fareast-theme-font:major-fareast;mso-hansi-font-family:Calibri;
mso-hansi-theme-font:major-latin;mso-fareast-language:ZH-CN'>四、商品期货套期保值的风险分析</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></h1>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>公司及下属子公司开展期货套期保值业务不以盈利为目的，主要为有效规避原材料市场价格剧烈波动对其经营带来的影响，但同时也会存在一定的风险，具体如下：</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<h2><span style='font-family:宋体;mso-ascii-font-family:Calibri;mso-ascii-theme-font:
major-latin;mso-fareast-theme-font:major-fareast;mso-hansi-font-family:Calibri;
mso-hansi-theme-font:major-latin;mso-fareast-language:ZH-CN'>（一）价格波动风险</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></h2>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>当期货行情大幅度波动时，实际引发的价格变动与公司预测判断的价格波动相背离，造成期货交易的损失而产生的风险。</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<h2><span style='font-family:宋体;mso-ascii-font-family:Calibri;mso-ascii-theme-font:
major-latin;mso-fareast-theme-font:major-fareast;mso-hansi-font-family:Calibri;
mso-hansi-theme-font:major-latin;mso-fareast-language:ZH-CN'>（二）内部控制风险</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></h2>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>期货交易专业性较强，复杂程度较高，可能会产生由于内部控制体系不完善造成的风险。</span><span lang=EN
style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<h2><span style='font-family:宋体;mso-ascii-font-family:Calibri;mso-ascii-theme-font:
major-latin;mso-fareast-theme-font:major-fareast;mso-hansi-font-family:Calibri;
mso-hansi-theme-font:major-latin;mso-fareast-language:ZH-CN'>（三）交易对手违约风险</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></h2>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>期货价格出现不利的大幅波动时，交易对手可能违反合同的相关约定，取消产品订单，造成损失。</span><span lang=EN
style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<h2><span style='font-family:宋体;mso-ascii-font-family:Calibri;mso-ascii-theme-font:
major-latin;mso-fareast-theme-font:major-fareast;mso-hansi-font-family:Calibri;
mso-hansi-theme-font:major-latin;mso-fareast-language:ZH-CN'>（四）技术风险</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></h2>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>由于无法控制或不可预测的系统、网络、通讯故障等造成交易系统非正常运行，使交易指令出现延迟、中断或数据错误等问题，从而带来相应风险。</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<h2><span style='font-family:宋体;mso-ascii-font-family:Calibri;mso-ascii-theme-font:
major-latin;mso-fareast-theme-font:major-fareast;mso-hansi-font-family:Calibri;
mso-hansi-theme-font:major-latin;mso-fareast-language:ZH-CN'>（五）政策风险</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></h2>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>期货市场法律法规等政策如发生重大变化，可能引起市场波动或无法交易，从而带来风险。</span><span lang=EN
style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<h1><span style='font-family:宋体;mso-ascii-font-family:Calibri;mso-ascii-theme-font:
major-latin;mso-fareast-theme-font:major-fareast;mso-hansi-font-family:Calibri;
mso-hansi-theme-font:major-latin;mso-fareast-language:ZH-CN'>五、公司拟采取的风险控制措施</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></h1>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>为了应对商品期货套期保值业务带来的上述风险，公司拟采取的风险控制措施如下：</span><span lang=EN
style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>（一）公司已根据《深圳证券交易所创业板股票上市规则》、《深圳证券交易所创业板上市公司规范运作指引》及《公司章程》等有关规定，结合公司实际情况，制定了《期货套期保值业务管理制度》，对期货套期保值业务的审批权限及信息披露、内部操作流程、风险管理及处理程序等做出明确规定。公司将严格按照《期货套期保值业务管理制度》规定对各个环节进行控制。</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>（二）遵循锁定原材料价格风险、套期保值原则，且只针对公司经营从事的</span><span lang=EN style='mso-fareast-language:
ZH-CN'><o:p></o:p></span></p>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>相关期货交易品种进行操作，不做投机性、套利性期货交易操作。</span><span lang=EN style='mso-fareast-language:
ZH-CN'><o:p></o:p></span></p>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>（三）合理计划和安排使用保证金，保证期货套期保值过程正常进行。与此同时，合理选择保值月份，避免市场流动性风险。</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>（四）设立符合要求的计算机系统及相关设施，确保交易工作正常开展。当发生故障时，及时采取相应的处理措施以减少损失。</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>（五）在针对<span class=GramE>客户锁价进行</span>期货套期保值操作时，对客户的材料锁定数量和履约能力进行评估。小批量且没有违约风险的，实行一次购入套保合约；而对批量较大的客户将全面评估其履约付款能力，按一定的风险系数比例由公司期货套期保值业务工作小组分批进行套期保值操作，以达到降低风险的目的；另外，如果客户在价格出现不利变化时违约，公司还将采取必要的法律手段积极维护自身的合法权益。</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>（六）公司<span class=GramE>内审部定期</span>及不定期对期货套期保值交易业务进行检查，监督期货套期保值业务人员执行风险管理制度和风险管理工作程序，及时防范业务中的操作风险。</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<h1><span style='font-family:宋体;mso-ascii-font-family:Calibri;mso-ascii-theme-font:
major-latin;mso-fareast-theme-font:major-fareast;mso-hansi-font-family:Calibri;
mso-hansi-theme-font:major-latin;mso-fareast-language:ZH-CN'>六、对公司的影响</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></h1>

<h2><span style='font-family:宋体;mso-ascii-font-family:Calibri;mso-ascii-theme-font:
major-latin;mso-fareast-theme-font:major-fareast;mso-hansi-font-family:Calibri;
mso-hansi-theme-font:major-latin;mso-fareast-language:ZH-CN'>（一）对公司生产经营的影响</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></h2>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>公司及下属子公司开展期货套期保值业务，充分利用期货工具的套期保值功能，合理规避和防范主要原材料价格波动对公司整体经营业绩的影响，有利于降低公司经营风险。</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<h2><span style='font-family:宋体;mso-ascii-font-family:Calibri;mso-ascii-theme-font:
major-latin;mso-fareast-theme-font:major-fareast;mso-hansi-font-family:Calibri;
mso-hansi-theme-font:major-latin;mso-fareast-language:ZH-CN'>（二）对公司财务的影响</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></h2>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>公司及下属子公司期货套期保值业务相关会计政策及核算将严格按照中华人民共和国财政部发布的《企业会计准则</span><span lang=EN
style='mso-fareast-language:ZH-CN'>—</span><span style='font-family:宋体;
mso-ascii-font-family:Cambria;mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:
minor-fareast;mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;
mso-fareast-language:ZH-CN'>金融工具确认和计量》及《企业会计准则</span><span lang=EN
style='mso-fareast-language:ZH-CN'>—</span><span style='font-family:宋体;
mso-ascii-font-family:Cambria;mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:
minor-fareast;mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;
mso-fareast-language:ZH-CN'>套期保值》等相关规定执行。</span><span lang=EN style='mso-fareast-language:
ZH-CN'><o:p></o:p></span></p>

<h1><span style='font-family:宋体;mso-ascii-font-family:Calibri;mso-ascii-theme-font:
major-latin;mso-fareast-theme-font:major-fareast;mso-hansi-font-family:Calibri;
mso-hansi-theme-font:major-latin;mso-fareast-language:ZH-CN'>七、结论</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></h1>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>公司及下属子公司开展期货套期保值业务，不以投机和套利交易为目的，是借助期货市场的价格发现、风险对冲功能，规避市场价格波动给公司生产经营带来的风险，稳定利润水平，提升公司持续盈利能力和综合竞争能力。</span><span
lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>综上所述，公司及下属子公司开展期货套期保值业务是切实可行的，对公司的经营是有利的。</span><span lang=EN
style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>天海融合防务装备技术股份有限公司</span><span lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>董事会</span><span lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

<p class=MsoBodyText><span style='font-family:宋体;mso-ascii-font-family:Cambria;
mso-ascii-theme-font:minor-latin;mso-fareast-theme-font:minor-fareast;
mso-hansi-font-family:Cambria;mso-hansi-theme-font:minor-latin;mso-fareast-language:
ZH-CN'>二〇二一年十月二十七日</span><span lang=EN style='mso-fareast-language:ZH-CN'><o:p></o:p></span></p>

</div>

</body>

</html>"""
    # 文档树
    html = etree.HTML(html_content2)
    # 从excel中抽出来的大标题，可以是单行或多行的，但是必须得是list
    title = ["天海融合防务装备技术股份有限公司", "关于开展商品期货套期保值业务的可行性分析报告"]
    node_list = convert_html_to_line_json(html)
    universal_formatted_node = convert_to_universal_format(node_list, title)
    json_obj = universal_formatted_node.traverse()
    gold_obj = {
        "guid": "0",
        "label": NodeType.Root,
        "content": ["ROOT"],
        "children": [
            {
                "guid": "0.0",
                "label": NodeType.Heading,
                "content": ["天海融合防务装备技术股份有限公司", "关于开展商品期货套期保值业务的可行性分析报告"],
                "children": [
                    {
                        "guid": "0.0.0",
                        "label": NodeType.Heading,
                        "content": ["一、开展商品期货套期保值业务的目的"],
                        "children": [
                            {
                                "guid": "0.0.0.0",
                                "label": NodeType.Text,
                                "content": [
                                    "天海融合防务装备技术股份有限公司（以下简称“公司”或“天海防务”）主要从事船舶与海洋工程业务涵盖船海工程研发设计、工程咨询和工程监理、总装集成制造等，形成了全方位、多层次的技术服务体系，各业务间既相互独立经营，又协同发展，实现了良性的互动效应。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.1",
                                "label": NodeType.Text,
                                "content": [
                                    "在生产经营过程中，公司全资子公司江苏大津重工有限公司（以下简称“大津重工”）需采购大量钢板作为原材料，但受需求端持续回暖及供给端减产影响，今年以来国内钢板价格持续上涨。公司新能源业务自2021年4月以来开展了焦炭贸易业务。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.2",
                                "label": NodeType.Text,
                                "content": [
                                    "为加强大津重工生产经营的成本管理，为了有效防范新能源业务经营活动中焦炭价格波动的风险，保证订单成本的相对稳定，降低价格波动公司正常经营的影响，公司及下属子公司拟使用自有资金，开展包括钢材、焦炭等商品的期货套期保值业务，充分利用期货市场的套期保值功能，降低原材料市场价格波动对公司生产经营成本的影响，有效控制市场风险，不以逐利为目的进行投机交易，有利于提升公司整体抵御风险的能力，增强财务稳健性。"
                                ],
                                "children": [],
                            },
                        ],
                    },
                    {
                        "guid": "0.0.1",
                        "label": NodeType.Heading,
                        "content": ["二、开展商品期货套期保值业务基本情况"],
                        "children": [
                            {
                                "guid": "0.0.1.0",
                                "label": NodeType.Heading,
                                "content": ["（一）期货套期保值交易品种"],
                                "children": [
                                    {
                                        "guid": "0.0.1.0.0",
                                        "label": NodeType.Text,
                                        "content": [
                                            "公司及下属子公司拟申请开展的期货套期保值业务将只限于在境内期货交易所交易的钢材及焦炭期货品种，严禁进行以盈利为目的的任何投机交易。"
                                        ],
                                        "children": [],
                                    }
                                ],
                            },
                            {
                                "guid": "0.0.1.1",
                                "label": NodeType.Heading,
                                "content": ["（二）投资期限"],
                                "children": [
                                    {
                                        "guid": "0.0.1.1.0",
                                        "label": NodeType.Text,
                                        "content": ["拟自本次董事会审议通过之日起至2021年年度董事会召开前有效。"],
                                        "children": [],
                                    }
                                ],
                            },
                            {
                                "guid": "0.0.1.2",
                                "label": NodeType.Heading,
                                "content": ["（三）预计交易数量、投入金额"],
                                "children": [
                                    {
                                        "guid": "0.0.1.2.0",
                                        "label": NodeType.Text,
                                        "content": [
                                            "公司及下属子公司将根据实际情况，开展钢材期货套期保值业务，对合计不超过8,000吨钢材期货套期保值，总计投入保证金不超过（即授权有效期内任一"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.1.2.1",
                                        "label": NodeType.Text,
                                        "content": [
                                            "时点都不超过）800万元，在上述额度范围内，资金可循环使用；对合计不超过5,000吨焦炭期货套期保值，总计投入保证金不超过（即授权有效期内任一时点都不超过）800万元，在上述额度范围内，资金可循环使用。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.1.2.2",
                                        "label": NodeType.Text,
                                        "content": [
                                            "期货套期保值操作小组将根据市场情况分批投入保证金，不会对公司及下属子公司的经营资金产生较大影响。"
                                        ],
                                        "children": [],
                                    },
                                ],
                            },
                            {
                                "guid": "0.0.1.3",
                                "label": NodeType.Heading,
                                "content": ["（四）资金来源"],
                                "children": [
                                    {
                                        "guid": "0.0.1.3.0",
                                        "label": NodeType.Text,
                                        "content": ["自有资金。"],
                                        "children": [],
                                    }
                                ],
                            },
                        ],
                    },
                    {
                        "guid": "0.0.2",
                        "label": NodeType.Heading,
                        "content": ["三、开展商品期货套期保值业务的可行性分析"],
                        "children": [
                            {
                                "guid": "0.0.2.0",
                                "label": NodeType.Text,
                                "content": [
                                    "今年以来，铁矿石、铜、铝等大宗商品价格快速上涨，国内6mm造船板和20mm造船板价格一度达到7590元/吨和7120元/吨，同比上涨70.9%和79.3%。尽管近期钢材价格有所回落，但仍保持在6000元/吨以上的高位，广大造船企业承受着巨大成本压力。以钢材为重要原材料的大津重工如能适时开展钢材的套期保值业务，可有效减少钢板价格波动所带来的成本压力，有利于锁定预期利润、减少价格波动造成的损失，具有较强的可行性和必要性。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.2.1",
                                "label": NodeType.Text,
                                "content": [
                                    "与此同时，公司全资子公司上海佳豪沃金新能源有限公司（以下简称“沃金新能源”）根据经营需需求，于2021年4月以来开展了焦炭贸易业务，受国际形势动荡影响，大宗商品价格出现大幅波动，焦炭也波及其中，如沃金新能源合理利用期货工具，可有效减少焦炭价格波动带来的经营风险，有利于锁定预期利润和减少价格波动造成的损失，符合沃金新能源日常经营需要，存在可行性和必要性。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.2.2",
                                "label": NodeType.Text,
                                "content": [
                                    "公司董事会制定了《期货套期保值业务管理制度》，对期货套期保值业务的审批权限及信息披露、内部操作流程、风险管理及处理程序等做出明确规定，能够有效保障期货业务的顺利进行，并对风险形成有效控制。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.2.3",
                                "label": NodeType.Text,
                                "content": [
                                    "公司将成立期货套期保值领导小组，负责公司期货套期保值业务相关事宜。相关业务部门及子公司将成立具体期货套期保值操作小组，组织具有良好素质的专门人员负责期货业务的交易工作。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.2.4",
                                "label": NodeType.Text,
                                "content": ["公司及下属子公司具备与期货套期保值业务的交易保证金相匹配的自有资金。"],
                                "children": [],
                            },
                        ],
                    },
                    {
                        "guid": "0.0.3",
                        "label": NodeType.Heading,
                        "content": ["四、商品期货套期保值的风险分析"],
                        "children": [
                            {
                                "guid": "0.0.3.0",
                                "label": NodeType.Text,
                                "content": [
                                    "公司及下属子公司开展期货套期保值业务不以盈利为目的，主要为有效规避原材料市场价格剧烈波动对其经营带来的影响，但同时也会存在一定的风险，具体如下："
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.3.1",
                                "label": NodeType.Heading,
                                "content": ["（一）价格波动风险"],
                                "children": [
                                    {
                                        "guid": "0.0.3.1.0",
                                        "label": NodeType.Text,
                                        "content": [
                                            "当期货行情大幅度波动时，实际引发的价格变动与公司预测判断的价格波动相背离，造成期货交易的损失而产生的风险。"
                                        ],
                                        "children": [],
                                    }
                                ],
                            },
                            {
                                "guid": "0.0.3.2",
                                "label": NodeType.Heading,
                                "content": ["（二）内部控制风险"],
                                "children": [
                                    {
                                        "guid": "0.0.3.2.0",
                                        "label": NodeType.Text,
                                        "content": [
                                            "期货交易专业性较强，复杂程度较高，可能会产生由于内部控制体系不完善造成的风险。"
                                        ],
                                        "children": [],
                                    }
                                ],
                            },
                            {
                                "guid": "0.0.3.3",
                                "label": NodeType.Heading,
                                "content": ["（三）交易对手违约风险"],
                                "children": [
                                    {
                                        "guid": "0.0.3.3.0",
                                        "label": NodeType.Text,
                                        "content": [
                                            "期货价格出现不利的大幅波动时，交易对手可能违反合同的相关约定，取消产品订单，造成损失。"
                                        ],
                                        "children": [],
                                    }
                                ],
                            },
                            {
                                "guid": "0.0.3.4",
                                "label": NodeType.Heading,
                                "content": ["（四）技术风险"],
                                "children": [
                                    {
                                        "guid": "0.0.3.4.0",
                                        "label": NodeType.Text,
                                        "content": [
                                            "由于无法控制或不可预测的系统、网络、通讯故障等造成交易系统非正常运行，使交易指令出现延迟、中断或数据错误等问题，从而带来相应风险。"
                                        ],
                                        "children": [],
                                    }
                                ],
                            },
                            {
                                "guid": "0.0.3.5",
                                "label": NodeType.Heading,
                                "content": ["（五）政策风险"],
                                "children": [
                                    {
                                        "guid": "0.0.3.5.0",
                                        "label": NodeType.Text,
                                        "content": [
                                            "期货市场法律法规等政策如发生重大变化，可能引起市场波动或无法交易，从而带来风险。"
                                        ],
                                        "children": [],
                                    }
                                ],
                            },
                        ],
                    },
                    {
                        "guid": "0.0.4",
                        "label": NodeType.Heading,
                        "content": ["五、公司拟采取的风险控制措施"],
                        "children": [
                            {
                                "guid": "0.0.4.0",
                                "label": NodeType.Text,
                                "content": ["为了应对商品期货套期保值业务带来的上述风险，公司拟采取的风险控制措施如下："],
                                "children": [],
                            },
                            {
                                "guid": "0.0.4.1",
                                "label": NodeType.Text,
                                "content": [
                                    "（一）公司已根据《深圳证券交易所创业板股票上市规则》、《深圳证券交易所创业板上市公司规范运作指引》及《公司章程》等有关规定，结合公司实际情况，制定了《期货套期保值业务管理制度》，对期货套期保值业务的审批权限及信息披露、内部操作流程、风险管理及处理程序等做出明确规定。公司将严格按照《期货套期保值业务管理制度》规定对各个环节进行控制。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.4.2",
                                "label": NodeType.Text,
                                "content": ["（二）遵循锁定原材料价格风险、套期保值原则，且只针对公司经营从事的"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.4.3",
                                "label": NodeType.Text,
                                "content": ["相关期货交易品种进行操作，不做投机性、套利性期货交易操作。"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.4.4",
                                "label": NodeType.Text,
                                "content": [
                                    "（三）合理计划和安排使用保证金，保证期货套期保值过程正常进行。与此同时，合理选择保值月份，避免市场流动性风险。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.4.5",
                                "label": NodeType.Text,
                                "content": [
                                    "（四）设立符合要求的计算机系统及相关设施，确保交易工作正常开展。当发生故障时，及时采取相应的处理措施以减少损失。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.4.6",
                                "label": NodeType.Text,
                                "content": [
                                    "（五）在针对客户锁价进行期货套期保值操作时，对客户的材料锁定数量和履约能力进行评估。小批量且没有违约风险的，实行一次购入套保合约；而对批量较大的客户将全面评估其履约付款能力，按一定的风险系数比例由公司期货套期保值业务工作小组分批进行套期保值操作，以达到降低风险的目的；另外，如果客户在价格出现不利变化时违约，公司还将采取必要的法律手段积极维护自身的合法权益。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.4.7",
                                "label": NodeType.Text,
                                "content": [
                                    "（六）公司内审部定期及不定期对期货套期保值交易业务进行检查，监督期货套期保值业务人员执行风险管理制度和风险管理工作程序，及时防范业务中的操作风险。"
                                ],
                                "children": [],
                            },
                        ],
                    },
                    {
                        "guid": "0.0.5",
                        "label": NodeType.Heading,
                        "content": ["六、对公司的影响"],
                        "children": [
                            {
                                "guid": "0.0.5.0",
                                "label": NodeType.Heading,
                                "content": ["（一）对公司生产经营的影响"],
                                "children": [
                                    {
                                        "guid": "0.0.5.0.0",
                                        "label": NodeType.Text,
                                        "content": [
                                            "公司及下属子公司开展期货套期保值业务，充分利用期货工具的套期保值功能，合理规避和防范主要原材料价格波动对公司整体经营业绩的影响，有利于降低公司经营风险。"
                                        ],
                                        "children": [],
                                    }
                                ],
                            },
                            {
                                "guid": "0.0.5.1",
                                "label": NodeType.Heading,
                                "content": ["（二）对公司财务的影响"],
                                "children": [
                                    {
                                        "guid": "0.0.5.1.0",
                                        "label": NodeType.Text,
                                        "content": [
                                            "公司及下属子公司期货套期保值业务相关会计政策及核算将严格按照中华人民共和国财政部发布的《企业会计准则—金融工具确认和计量》及《企业会计准则—套期保值》等相关规定执行。"
                                        ],
                                        "children": [],
                                    }
                                ],
                            },
                        ],
                    },
                    {
                        "guid": "0.0.6",
                        "label": NodeType.Heading,
                        "content": ["七、结论"],
                        "children": [
                            {
                                "guid": "0.0.6.0",
                                "label": NodeType.Text,
                                "content": [
                                    "公司及下属子公司开展期货套期保值业务，不以投机和套利交易为目的，是借助期货市场的价格发现、风险对冲功能，规避市场价格波动给公司生产经营带来的风险，稳定利润水平，提升公司持续盈利能力和综合竞争能力。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.6.1",
                                "label": NodeType.Text,
                                "content": [
                                    "综上所述，公司及下属子公司开展期货套期保值业务是切实可行的，对公司的经营是有利的。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.6.2",
                                "label": NodeType.Text,
                                "content": ["天海融合防务装备技术股份有限公司"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.6.3",
                                "label": NodeType.Text,
                                "content": ["董事会"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.6.4",
                                "label": NodeType.Text,
                                "content": ["二〇二一年十月二十七日"],
                                "children": [],
                            },
                        ],
                    },
                ],
            }
        ],
    }

    assert json_obj == gold_obj


def test_parse_with_prefix():
    html_content = """
    <h1>Heading 1</h1>
        <h2>#####Text1</h2>
        <h2>#####Text2</h2>
        <h2>Heading 1.1</h2>
            <p>Text 3</p>
        <h2>#####Text4</h2>
        <h2>#####Text5</h2>
        <h2>Heading 1.2</h2>
            <p>Text 6</p>
            <p>Text 7</p>
        <h2>#####Text8</h2>
        <h2>#####Text9</h2>
    <h1>Heading 2</h1>
        <h2>#####Text10</h2>
        <h2>#####Text11</h2>
    """

    # 文档树
    html = etree.HTML(html_content)
    # 从excel中抽出来的大标题，可以是单行或多行的，但是必须得是list
    title = ["Main Title", "--Second Line Title"]
    node_list = convert_html_to_line_json(html)
    universal_formatted_node = convert_to_universal_format_with_xfix(
        title, node_list, prefix="#####"
    )
    json_obj = universal_formatted_node.traverse()
    gold_obj = {
        "guid": "0",
        "label": NodeType.Root,
        "content": ["ROOT"],
        "children": [
            {
                "guid": "0.0",
                "label": NodeType.Heading,
                "content": ["Main Title", "--Second Line Title"],
                "children": [
                    {
                        "guid": "0.0.0",
                        "label": NodeType.Heading,
                        "content": ["Heading 1"],
                        "children": [
                            {
                                "guid": "0.0.0.0",
                                "label": NodeType.Text,
                                "content": ["Text1"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.1",
                                "label": NodeType.Text,
                                "content": ["Text2"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.2",
                                "label": NodeType.Heading,
                                "content": ["Heading 1.1"],
                                "children": [
                                    {
                                        "guid": "0.0.0.2.0",
                                        "label": NodeType.Text,
                                        "content": ["Text 3"],
                                        "children": [],
                                    }
                                ],
                            },
                            {
                                "guid": "0.0.0.3",
                                "label": NodeType.Text,
                                "content": ["Text4"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.4",
                                "label": NodeType.Text,
                                "content": ["Text5"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.5",
                                "label": NodeType.Heading,
                                "content": ["Heading 1.2"],
                                "children": [
                                    {
                                        "guid": "0.0.0.5.0",
                                        "label": NodeType.Text,
                                        "content": ["Text 6"],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.0.5.1",
                                        "label": NodeType.Text,
                                        "content": ["Text 7"],
                                        "children": [],
                                    },
                                ],
                            },
                            {
                                "guid": "0.0.0.6",
                                "label": NodeType.Text,
                                "content": ["Text8"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.7",
                                "label": NodeType.Text,
                                "content": ["Text9"],
                                "children": [],
                            },
                        ],
                    },
                    {
                        "guid": "0.0.1",
                        "label": NodeType.Heading,
                        "content": ["Heading 2"],
                        "children": [
                            {
                                "guid": "0.0.1.0",
                                "label": NodeType.Text,
                                "content": ["Text10"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.1.1",
                                "label": NodeType.Text,
                                "content": ["Text11"],
                                "children": [],
                            },
                        ],
                    },
                ],
            }
        ],
    }
    assert json_obj == gold_obj


def test_parse_with_suffix():
    html_content = """
    <h1>Heading 1</h1>
        <h2>Text1。</h2>
        <h2>Text2。</h2>
        <h2>Heading 1.1</h2>
            <p>Text 3</p>
        <h2>Text4。</h2>
        <h2>Text5。</h2>
        <h2>Heading 1.2</h2>
            <p>Text 6</p>
            <p>Text 7</p>
        <h2>Text8。</h2>
        <h2>Text9。</h2>
    <h1>Heading 2</h1>
        <h2>Text10。</h2>
        <h2>Text11。</h2>
    """

    # 文档树
    html = etree.HTML(html_content)
    # 从excel中抽出来的大标题，可以是单行或多行的，但是必须得是list
    title = ["Main Title", "--Second Line Title"]
    node_list = convert_html_to_line_json(html)
    universal_formatted_node = convert_to_universal_format_with_xfix(
        title, node_list, suffix="。"
    )
    json_obj = universal_formatted_node.traverse()
    gold_obj = {
        "guid": "0",
        "label": NodeType.Root,
        "content": ["ROOT"],
        "children": [
            {
                "guid": "0.0",
                "label": NodeType.Heading,
                "content": ["Main Title", "--Second Line Title"],
                "children": [
                    {
                        "guid": "0.0.0",
                        "label": NodeType.Heading,
                        "content": ["Heading 1"],
                        "children": [
                            {
                                "guid": "0.0.0.0",
                                "label": NodeType.Text,
                                "content": ["Text1"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.1",
                                "label": NodeType.Text,
                                "content": ["Text2"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.2",
                                "label": NodeType.Heading,
                                "content": ["Heading 1.1"],
                                "children": [
                                    {
                                        "guid": "0.0.0.2.0",
                                        "label": NodeType.Text,
                                        "content": ["Text 3"],
                                        "children": [],
                                    }
                                ],
                            },
                            {
                                "guid": "0.0.0.3",
                                "label": NodeType.Text,
                                "content": ["Text4"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.4",
                                "label": NodeType.Text,
                                "content": ["Text5"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.5",
                                "label": NodeType.Heading,
                                "content": ["Heading 1.2"],
                                "children": [
                                    {
                                        "guid": "0.0.0.5.0",
                                        "label": NodeType.Text,
                                        "content": ["Text 6"],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.0.5.1",
                                        "label": NodeType.Text,
                                        "content": ["Text 7"],
                                        "children": [],
                                    },
                                ],
                            },
                            {
                                "guid": "0.0.0.6",
                                "label": NodeType.Text,
                                "content": ["Text8"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.7",
                                "label": NodeType.Text,
                                "content": ["Text9"],
                                "children": [],
                            },
                        ],
                    },
                    {
                        "guid": "0.0.1",
                        "label": NodeType.Heading,
                        "content": ["Heading 2"],
                        "children": [
                            {
                                "guid": "0.0.1.0",
                                "label": NodeType.Text,
                                "content": ["Text10"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.1.1",
                                "label": NodeType.Text,
                                "content": ["Text11"],
                                "children": [],
                            },
                        ],
                    },
                ],
            }
        ],
    }
    assert json_obj == gold_obj


def test_parse_with_prefix_and_suffix():
    html_content = """
    <h1>Heading 1</h1>
        <h2>###Text1。</h2>
        <h2>###Text2。</h2>
        <h2>Heading 1.1</h2>
            <p>Text 3</p>
        <h2>###Text4。</h2>
        <h2>###Text5。</h2>
        <h2>Heading 1.2</h2>
            <p>Text 6</p>
            <p>Text 7</p>
        <h2>###Text8。</h2>
        <h2>###Text9。</h2>
    <h1>Heading 2</h1>
        <h2>###Text10。</h2>
        <h2>###Text11。</h2>
    """

    # 文档树
    html = etree.HTML(html_content)
    # 从excel中抽出来的大标题，可以是单行或多行的，但是必须得是list
    title = ["Main Title", "--Second Line Title"]
    node_list = convert_html_to_line_json(html)
    universal_formatted_node = convert_to_universal_format_with_xfix(
        title, node_list, prefix="###", suffix="。"
    )
    json_obj = universal_formatted_node.traverse()
    gold_obj = {
        "guid": "0",
        "label": NodeType.Root,
        "content": ["ROOT"],
        "children": [
            {
                "guid": "0.0",
                "label": NodeType.Heading,
                "content": ["Main Title", "--Second Line Title"],
                "children": [
                    {
                        "guid": "0.0.0",
                        "label": NodeType.Heading,
                        "content": ["Heading 1"],
                        "children": [
                            {
                                "guid": "0.0.0.0",
                                "label": NodeType.Text,
                                "content": ["Text1"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.1",
                                "label": NodeType.Text,
                                "content": ["Text2"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.2",
                                "label": NodeType.Heading,
                                "content": ["Heading 1.1"],
                                "children": [
                                    {
                                        "guid": "0.0.0.2.0",
                                        "label": NodeType.Text,
                                        "content": ["Text 3"],
                                        "children": [],
                                    }
                                ],
                            },
                            {
                                "guid": "0.0.0.3",
                                "label": NodeType.Text,
                                "content": ["Text4"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.4",
                                "label": NodeType.Text,
                                "content": ["Text5"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.5",
                                "label": NodeType.Heading,
                                "content": ["Heading 1.2"],
                                "children": [
                                    {
                                        "guid": "0.0.0.5.0",
                                        "label": NodeType.Text,
                                        "content": ["Text 6"],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.0.5.1",
                                        "label": NodeType.Text,
                                        "content": ["Text 7"],
                                        "children": [],
                                    },
                                ],
                            },
                            {
                                "guid": "0.0.0.6",
                                "label": NodeType.Text,
                                "content": ["Text8"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.7",
                                "label": NodeType.Text,
                                "content": ["Text9"],
                                "children": [],
                            },
                        ],
                    },
                    {
                        "guid": "0.0.1",
                        "label": NodeType.Heading,
                        "content": ["Heading 2"],
                        "children": [
                            {
                                "guid": "0.0.1.0",
                                "label": NodeType.Text,
                                "content": ["Text10"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.1.1",
                                "label": NodeType.Text,
                                "content": ["Text11"],
                                "children": [],
                            },
                        ],
                    },
                ],
            }
        ],
    }
    assert json_obj == gold_obj


def test_parse_bid_html():
    test_content = """<p class="MsoListParagraph" style="line-height: 150%; margin-left: 25px;"> <span
            style="line-height: 150%; font-family: 宋体;">本招标项目<font style="text-decoration:underline;">
                河北建设投资集团有限责任公司在老挝投资建设60MW怀拉涅河水力发电项目</font>已由<font style="text-decoration:underline;">
                河北省发展和改革委员会</font>以<font style="text-decoration:underline;">冀发改外资备【2017】32号</font>批准建设，项目业主为
            <font style="text-decoration:underline;">Houay LaNge Power Co,Ltd</font>，建设资金来自<font
                style="text-decoration:underline;">企业自筹</font>，项目出资比例为<font
                style="text-decoration:underline;">100%</font>，招标人为<font style="text-decoration:underline;">
                建投国际投资有限公司</font>。项目已具备招标条件，现对该项目的设计施工总承包进行公开招标。
        </span> </p>"""
    title = ["老挝怀拉捏河水电项目-新建 H.La-Nge 水电站至 Nam E-Moun 变电站 220kV 单回路输电线路EPC总承包工程（二次）招标公告"]
    root = convert_html_string_with_xfix(test_content, title)
    json_obj = root.traverse()
    gold_obj = {
        "guid": "0",
        "label": NodeType.Root,
        "content": ["ROOT"],
        "children": [
            {
                "guid": "0.0",
                "label": NodeType.Heading,
                "content": [
                    "老挝怀拉捏河水电项目-新建 H.La-Nge 水电站至 Nam E-Moun 变电站 220kV 单回路输电线路EPC总承包工程（二次）招标公告"
                ],
                "children": [
                    {
                        "guid": "0.0.0",
                        "label": NodeType.Text,
                        "content": [
                            "本招标项目河北建设投资集团有限责任公司在老挝投资建设60MW怀拉涅河水力发电项目已由河北省发展和改革委员会以冀发改外资备【2017】32号批准建设，项目业主为Houay LaNge Power Co,Ltd，建设资金来自企业自筹，项目出资比例为100%，招标人为建投国际投资有限公司。项目已具备招标条件，现对该项目的设计施工总承包进行公开招标。"
                        ],
                        "children": [],
                    }
                ],
            }
        ],
    }

    assert json_obj == gold_obj


def test_convert_node_to_html():
    html_content = """
    <h1>Heading 1</h1>
        <h2>###Text1。</h2>
        <h2>###Text2。</h2>
        <h2>Heading 1.1</h2>
            <p>Text 3</p>
        <h2>###Text4。</h2>
        <h2>###Text5。</h2>
        <h2>Heading 1.2</h2>
            <p>Text 6</p>
            <p>Text 7</p>
        <h2>###Text8。</h2>
        <h2>###Text9。</h2>
    <h1>Heading 2</h1>
        <h2>###Text10。</h2>
        <h2>###Text11。</h2>
    """
    # 文档树
    html = etree.HTML(html_content)
    # 从excel中抽出来的大标题，可以是单行或多行的，但是必须得是list
    title = ["Main Title", "--Second Line Title"]
    node_list = convert_html_to_line_json(html)
    universal_formatted_node = convert_to_universal_format_with_xfix(
        title, node_list, prefix="###", suffix="。"
    )
    assert (
        convert_node_to_html(universal_formatted_node)
        == "<h1>Main Title--Second Line Title</h1><h2>Heading 1</h2><p>Text1</p><p>Text2</p><h3>Heading 1.1</h3><p>Text 3</p><p>Text4</p><p>Text5</p><h3>Heading 1.2</h3><p>Text 6</p><p>Text 7</p><p>Text8</p><p>Text9</p><h2>Heading 2</h2><p>Text10</p><p>Text11</p>"
    )


def test_text_between_headings():
    html_content = """
    <p>Text before heading 1</p>
    <h1>Heading 1</h1>
        <p>Text after heading 1</p>
        <h2>###Text1。</h2>
        <h2>###Text2。</h2>
        <h2>Heading 1.1</h2>
            <p>Text 3</p>
        <h2>###Text4。</h2>
        <h2>###Text5。</h2>
        <h2>Heading 1.2</h2>
            <p>Text 6</p>
            <p>Text 7</p>
        <h2>###Text8。</h2>
        <h2>###Text9。</h2>
    <h1>Heading 2</h1>
        <h2>###Text10。</h2>
        <h2>###Text11。</h2>
    """
    # 文档树
    html = etree.HTML(html_content)
    # 从excel中抽出来的大标题，可以是单行或多行的，但是必须得是list
    title = ["Main Title", "--Second Line Title"]
    node_list = convert_html_to_line_json(html)
    universal_formatted_node = convert_to_universal_format_with_xfix(
        title, node_list, prefix="###", suffix="。"
    )
    json_obj = universal_formatted_node.traverse()
    gold_obj = {
        "guid": "0",
        "label": NodeType.Root,
        "content": ["ROOT"],
        "children": [
            {
                "guid": "0.0",
                "label": NodeType.Heading,
                "content": ["Main Title", "--Second Line Title"],
                "children": [
                    {
                        "guid": "0.0.0",
                        "label": NodeType.Text,
                        "content": ["Text before heading 1"],
                        "children": [],
                    },
                    {
                        "guid": "0.0.1",
                        "label": NodeType.Heading,
                        "content": ["Heading 1"],
                        "children": [
                            {
                                "guid": "0.0.1.0",
                                "label": NodeType.Text,
                                "content": ["Text after heading 1"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.1.1",
                                "label": NodeType.Text,
                                "content": ["Text1"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.1.2",
                                "label": NodeType.Text,
                                "content": ["Text2"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.1.3",
                                "label": NodeType.Heading,
                                "content": ["Heading 1.1"],
                                "children": [
                                    {
                                        "guid": "0.0.1.3.0",
                                        "label": NodeType.Text,
                                        "content": ["Text 3"],
                                        "children": [],
                                    }
                                ],
                            },
                            {
                                "guid": "0.0.1.4",
                                "label": NodeType.Text,
                                "content": ["Text4"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.1.5",
                                "label": NodeType.Text,
                                "content": ["Text5"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.1.6",
                                "label": NodeType.Heading,
                                "content": ["Heading 1.2"],
                                "children": [
                                    {
                                        "guid": "0.0.1.6.0",
                                        "label": NodeType.Text,
                                        "content": ["Text 6"],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.1.6.1",
                                        "label": NodeType.Text,
                                        "content": ["Text 7"],
                                        "children": [],
                                    },
                                ],
                            },
                            {
                                "guid": "0.0.1.7",
                                "label": NodeType.Text,
                                "content": ["Text8"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.1.8",
                                "label": NodeType.Text,
                                "content": ["Text9"],
                                "children": [],
                            },
                        ],
                    },
                    {
                        "guid": "0.0.2",
                        "label": NodeType.Heading,
                        "content": ["Heading 2"],
                        "children": [
                            {
                                "guid": "0.0.2.0",
                                "label": NodeType.Text,
                                "content": ["Text10"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.2.1",
                                "label": NodeType.Text,
                                "content": ["Text11"],
                                "children": [],
                            },
                        ],
                    },
                ],
            }
        ],
    }
    assert json_obj == gold_obj


def test_text_between_headings_real():
    html_string = """
    <!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="" xml:lang="">
<head>
  <meta charset="utf-8" />
  <meta name="generator" content="pandoc" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
  <title>1</title>
  <style type="text/css">
      code{white-space: pre-wrap;}
      span.smallcaps{font-variant: small-caps;}
      span.underline{text-decoration: underline;}
      div.column{display: inline-block; vertical-align: top; width: 50%;}
  </style>
  <!--[if lt IE 9]>
    <script src="//cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.3/html5shiv-printshiv.min.js"></script>
  <![endif]-->
</head>
<body>
<h1 id="声明">声明</h1>
<blockquote>
<p>本评级机构对 2021 年山东省政府交通能源市政产业园基础设施及民生社会事业发展专项债券（一至四期）—2021 年山东省政府专项债券（一至四期）的信用评级作如下声明：</p>
<p>本次债券信用评级的评级结论是本评级机构以及评级分析员在履行尽职调查基础上，根据本评级机构的地方政府债券信用评级标准和程序做出的独立判断。本次评级所依据的评级方法是新世纪评级《中国地方政府专项债券信用评级方法》。上述评级方法可于新世纪评级官方网站查询。</p>
<p>本评级机构及本次地方政府债券信用评级分析员与债务人之间不存在除本次信用评级事项委托关系以外的任何影响评级行为独立、客观、公正的关联关系，并在信用评级过程中恪守诚信原则，保证出具的评级报告客观、公正、准确、及时。</p>
<p>本评级机构的信用评级和其后的跟踪评级均依据地方政府所提供的资料，地方政府对其提供资料的合法性、真实性、完整性、准确性负责。</p>
<p>鉴于信用评级的及时性，本评级机构将对地方政府债券进行跟踪评级。在信用等级有效期限内，地方政府在财政、地方经济外部经营环境等发生重大变化时应及时向本评级机构提供相关资料，本评级机构将按照相关评级业务规范，进行后续跟踪评级，并保留变更及公告信用等级的权利。</p>
<p>本次地方政府债券信用评级结论不是引导投资者买卖或者持有地方政府发行的各类金融产品，以及债权人向地方政府授信、放贷或赊销的建议， 也不是对与地方政府相关金融产品或债务定价作出的相应评论。</p>
<p>本评级报告所涉及的有关内容及数字分析均属敏感性商业资料，其版权归本评级机构所有，未经授权不得修改、复制、转载、散发、出售或以任何方式外传。</p>
</blockquote>
<h1 id="释义">释义</h1>
<blockquote>
<p>新世纪评级，或本评级机构：上海新世纪资信评估投资服务有限公司</p>
<p>本批债券：2021 年山东省政府交通能源市政产业园基础设施及民生社会事业发展专项债券（一至四期）—2021 年山东省政府专项债券（一至四期）</p>
</blockquote>
<h1 id="一山东省政府信用质量分析">一、山东省政府信用质量分析</h1>
<h2 id="一-山东省经济实力">（一） 山东省经济实力</h2>
<p>近年来，山东省地区生产总值保持增长趋势，综合实力位居全国前 列。作为工业和农业大省，山东省经济基础较好，产业竞争力较强；科技创新、丰富的人力资源和自然资源可为山东省经济发展提供较高保障； 但同时也持续面临着产业结构转型升级下的落后产能淘汰压力以及节 能环保压力。投资和消费是拉动全省经济增长的主要动力，近年来山东省投资结构和消费结构持续优化。</p>
<blockquote>
<p>山东省地处我国胶东半岛，位于渤海、黄海之间，黄河横贯东西， 大运河纵穿南北，是我国重要的工业、农业和人口大省。全省土地面积</p>
<p>15.8 万平方公里，占全国的 1.6%。行政区划方面，截至 2020 年末，山东省下辖济南市、青岛市两个副省级市，以及淄博市、枣庄市、东营市、烟台市、潍坊市、济宁市、泰安市、威海市、日照市、临沂市、德州市、聊城市、滨州市和菏泽市十四个地级市。2019 年末，全省常住人口 1.01 亿人，占全国总人口的 7.19%。</p>
<p>依托区位优势及丰富的劳动力资源等，山东省产业基础稳固，近年全省经济发展水平维持在全国先地位，但受新旧动能转换、去产能、环保趋严、新冠肺炎疫情冲击等因素影响，经济增速逐年下滑。</p>
<p>2018-2020 年，山东省分别实现地区生产总值 6.66 万亿元、7.11 万亿元和 7.31 万亿元，按可比价格计算，分别比上年增长 6.3%、5.5%和 3.6%。从三次产业结构看，2020 年山东省第一产业增加值为 0.54 万亿元，同比增长 2.7%；第二产业增加值为 2.86 万亿元，同比增长 3.3%；第三产业增加值为 3.92 万亿元，同比增长 3.9%。2020 年，山东省三次产业结构比例由上年的 7.2：39.8：53.0 调整为 7.3：39.1：53.6。</p>
<p>山东省拥有天然的地理区位优势和资源禀赋，已发现矿产种类 148 种，其中黄金、石油、铁矿石、煤炭、菱镁矿等矿产资源基础储量丰富， 全国排名前列。山东省近海海域占渤海和黄海总面积的 37%，滩涂面积占全国的 15%，是国内水产品和原盐的主产地之一。依靠优越的地理位置和丰富的自然资源，山东省长期以来一直是我国重要的农业大省，地区主要产品原盐、水产品、原油、棉花、油料等产量占全国的比重均处于较高水平。2020 年山东省农林牧渔业总产值为 1.02 万亿元，同比增长 3.0%，成为全国首个农业总产值过万亿元的省份；粮食总产量 5446.8 万吨，同比增长 1.7%，占全国粮食产量的 8.1%；当年，水产品总产量为 790.2 万吨，占全国水产品总产量的 12.1%，其中海水产品产量 679.5 万吨。</p>
<p>山东省制造业基础较好，工业体量持续位居全国前列，但全省工业结构仍以重工业和传统行业为主，行业发展处于价值链中低端，面临较大环境保护、技术升级转型等压力。在此背景下，近年来全省持续推动新旧动能转换工程，化解钢铁、煤炭、电解铝、火电、建材等高耗能行业过剩产能，不断培育以新一代信息技术、高端装备、新能源新材料、现代海洋、医养健康等行业为主的新动能，目前动能转换已初见成效， 业经济增速整体有所提升。2020 年，山东省工业增加值为 2.31 万亿</p>
<p>元，同比增长 3.6%，增速较上年提高 1.5 个百分点。从新旧动能转换看， 2020 年全省压减焦化产能 729 万吨，退出地炼产能 1176 万吨；高新技术产业产值占规模以上工业产值比重为 45.1%，较上年提高 5.0 个百分点；新一代信息技术制造业、新能源新材料、高端装备等十强产业增加值分别增长 14.5%、19.6%和 9.0%，依次高于规模以上工业增加值增速</p>
<p>9.5 个、14.6 个和 4.0 个百分点；光电子器件、服务器、半导体分立器件、碳纤维、工业机器人等高端智能产品产量分别增长 24.8%、35.3%、15.5%、129.5%和 24.9%。</p>
<p>服务业方面，近年来山东省服务业保持较快发展态势，服务业主导型经济结构进一步巩固。2020 年山东省服务业实现增加值3.92 万亿元， 占全省生产总值比重为 53.6%，较上年提高 0.8 个百分点；对经济增长的贡献率为 55.1%。同时，山东省持续推动服务业转型与发展，服务业新动能增势强劲。2020 年山东省规模以上服务业营业收入增长 3.5%， 其中，高技术服务业营业收入增长 11.5%。</p>
<p>经济发展驱动力方面，投资和消费是拉动经济增长的主要动力，近年来山东省投资结构和消费结构持续优化。投资方面，2020 年山东省固定资产投资同比增长 3.6%，三次产业投资结构为 2.3：31.3：66.4。在重点投资领域中，2020 年山东省制造业投资增长 7.6%，对全部投资增长贡献率为 51.9%；高技术产业投资增长 21.6%，其中高技术制造业和服务业投资分别增长 38.1%和 8.4%。消费方面，2020 年山东省社会消费品零售总额 2.92 万亿元，较上年基本持平。从消费结构看，2020</p>
<p>年山东省智能家电和音像器材、新能源汽车较上年分别增长 1.6 倍和49.1%，能效等级 1、2 级家电商品增长 80.8%。从消费方式看，2020 年山东省实现网上零售额 4613.3 亿元，较上年增长 13.8%。</p>
<p>作为我国最早开放的十四个沿海省份之一，山东省也是我国对外贸易的重要口岸之一，但近年来受全球经济变化和国内供需变动等因素影响，全省对外贸易情况有所波动。2020 年山东省进出口总额 2.20 万亿元，同比增长 7.5%，其中出口额为 1.31 万亿元，同比增长 17.3%；进口额为 0.90 万亿元，同比下降 4.1%。</p>
<p>区域发展方面，山东省有 7 个市为沿海城市，目前已形成山东半岛蓝色经济区、黄河三角洲高效生态经济区、省会城市经济圈以及西部经济隆起带的发展格局。从各经济区的发展规划看，山东半岛蓝色经济区要发展海洋经济；省会城市群经济圈主要依托省会城市优势带动周边地区发展；黄河三角洲高效生态经济区主要发展高效和循环经济；西部</p>
<p>经济隆起带主要致力于建设具有较强竞争力的特色产业基地1，使西部地区成为山东经济发展新引擎。四大经济区均依托自身优势，协调发展， 共同推动山东省产业结构转型和升级。此外，2018 年 1 月，国务院正式批复《山东新旧动能转换综合试验区建设总体方案》，同意设立山东新旧动能转换综合试验区，该区位于山东省全境，包括济南、青岛、烟台三大核心城市，十四个设区市的国家和省级经济技术开发区、高新技术产业开发区以及海关特殊监管区域，形成“三核引领、多点突破、融合互动”的新旧动能转换总体布局。</p>
<p>未来，山东省将继续致力于经济结构调整，实施高端高质高效的产业发展战略，推动传统产业向中高端迈进，发展现代制造业和新兴服务业，经济结构有望进一步优化。第一产业方面，山东省将持续推进千亿斤粮食产能建设，实施“渤海粮仓”科技工程和耕地质量提升计划，努力实现粮食生产稳步增长和农业生产现代化。第二产业方面，山东省将加快信息技术与传统制造业跨界融合，培育智能制造、协同制造、绿色制造、增材制造等新业态，促进传统制造业转型升级；加大新兴产业领军企业引导力度，鼓励各区域发挥特色优势，增强高端制造业的整体竞争力；此外，山东省将加快园区升级，创建国家生态工业示范园区，培育创新型产业集群。第三产业方面，在加快发展技术含量和附加值高的金融、物流、节能环保、电子商务等现代服务业的基础上，适应社会消费结构转型升级趋势，加快发展满足个性化、多样化消费需求的新兴服务业，支持发展健康服务业，树立“大旅游”理念，推动旅游产品标准化建设和定制化服务。</p>
</blockquote>
<h2 id="二-山东省财政实力">（二） 山东省财政实力</h2>
<p>山东省财政收入规模保持在较高水平，其中，可支配收入稳定性较高；一般公共预算收支自给能力较强，收支平衡对中央转移支付的依赖程度较小；国有土地使用权出让收入是政府性基金预算收入的主要组成部分，房地产市场和土地市场情况对基金预算收入产生一定影响。</p>
<p>2018-2020 年，山东省分别实现可支配收入<sup>2</sup>1.99 万亿元、2.18 万亿元和 2.51 万亿元，受益于较大规模国有土地使用权出让相关收入实现， 全省可支配收入持续增长。山东省可支配收入主要来源于一般公共预算</p>
<blockquote>
<p>收入总计，同期一般公共预算收入总计占可支配收入的比重分别为</p>
<p>59.83%、56.99%和 53.50%。</p>
</blockquote>
<h3 id="山东省一般公共预算收支情况">1.山东省一般公共预算收支情况</h3>
<blockquote>
<p>与经济发展水平相适应，山东省一般公共预算收入在全国处于较高水平，且近年来保持增长态势。2018-2020 年，山东省分别完成一般公共预算收入 6485.40 亿元、6526.71 亿元和 6559.90 亿元，同比分别增长6.3%、0.6%和 0.5%，受经济下行压力加大、实施更大规模减税降费以及新冠肺炎疫情冲击等因素影响，2019 年以来一般公共预算收入增速有所下降。考虑到上级补助收入、上年结余、债务收入及调入资金等因素后，2018-2020 年山东省一般公共预算收入总计分别为 11911.68 亿元、 12419.98 亿元和 13447.20 亿元。</p>
<p>从一般公共预算收入结构看，山东省一般公共预算收入以税收收入为主，2018-2020 年税收比率分别为 75.52%、74.30%和 72.53%，处于较高水平。2018-2020 年，山东省分别完成税收收入 4897.92 亿元、4849.29 亿元和 4757.59 亿元，同比分别增长 10.8%、-1.0%和-1.9%，2019年以来税收收入增速持续为负，主要系受全省落实减税降费以及新冠肺炎疫情冲击等因素影响。从税收结构看，山东省税种以增值税和所得税为主，2020 年增值税和企业所得税分别为 1814.47 亿元和 686.52 亿元，占当年税收收入的比重分别为 38.14%和 14.43%。</p>
<p>2018-2020 年，山东省非税收入分别完成 1587.47 亿元、1677.42 亿和 1802.31 亿元，同比分别增长-5.5%、5.7%和 7.4%，主要受减费降税等因素影响，2018 年非税收入有所下滑。山东省非税收入以行政事业性收费收入、专项收入和国有资源（资产）有偿使用收入为主，2020</p>
<p>年以上三项合计实现收入 1412.01 亿元，合计占当年非税收入的 78.34%。</p>
<p>2018-2020 年，山东省一般公共预算支出分别完成 10100.96 亿元、10739.76 亿元和 11231.17 亿元，同比分别增长 9.1%、6.3%和 4.6%。山东省一般公共预算支出主要集中于教育、社会保障和就业、农林水、城乡社区、一般公共服务和卫生健康等领域，各项重点支出得到有效保障。2018-2020 年，以上 6 个领域支出合计分别为 7197.20 亿元、7721.02 亿元和 8213.47 亿元，占全省一般公共预算支出的比重分别为 71.25%、71.89% 和 73.13%。2018-2020 年全省一般公共预算自给率<sup>3</sup> 分别为</p>
<p>64.21%、60.77%和 58.41%。考虑到上解上级支出、债券还本、调出资金及结转下年支出等因素后，2018-2020 年山东省一般公共预算支出总计与收入总计实现平衡。</p>
<p>3 一般公共预算自给率=一般公共预算收入/一般公共预算支出*100%，下同。</p>
<p>从省级一般公共预算收支情况看，2018-2020 年山东省级一般公共预算收入分别完成 236.20 亿元、235.53 亿元和 183.66 亿元，其中税收</p>
<p>收入分别为 129.56 亿元、117.99 亿元和 67.80 亿元，受减税降费以及新冠肺炎疫情冲击等因素影响，2019 年以来税收收入有所下降；同期， 非税收入分别为 106.64 亿元、117.54 亿元和 115.86 亿元。2018-2020 年， 山东省级一般公共预算支出分别完成 908.67 亿元、1075.84 亿元和1028.64 亿元，主要集中于教育、农林水、社会保障和就业等方面，省级一般公共预算收入对其一般公共预算支出覆盖程度较低。考虑上解上级支出、债券转贷支出及安排稳定调节基金等因素后，山东省省级一般公共预算支出总计与收入总计实现平衡。</p>
<p>青岛市于 1986 年 10 月获国务院批准成为计划单列市，并获得相当于省一级的经济管理权限，经济发展较好，财政实力较强。在一般公共预算收支不考虑青岛市的情况下，收入方面，2018-2020 年山东省（不含青岛）一般公共预算收入分别完成 5253.48 亿元、5284.97 亿元和5306.08 亿元。支出方面，2018-2020 年山东省（不含青岛）一般公共预</p>
<p>算支出分别完成 8541.18 亿元、9163.78 亿元和 9646.52 亿元，一般公共预算自给率分别为 61.51%、57.67%和 55.01%。考虑到上级补助收入、上年结余、上解上级支出、结转下年支出等因素后，2018-2020 年山东省（不含青岛）一般公共预算收入和支出总计实现平衡。</p>
</blockquote>
<h3 id="山东省政府性基金预算收支情况">2.山东省政府性基金预算收支情况</h3>
<blockquote>
<p>2018-2020 年，山东省政府性基金预算收入分别完成 6000.62 亿元、</p>
<p>6742.71 亿元和 7278.99 亿元，同比分别增长 59.2%、12.4%和 8.0%，其</p>
<p>中 2018 年政府性基金收入大幅增加，主要系国有土地使用权出让相关收入、国有土地收益基金相关收入和城市基础设施配套费收入等大幅增加所致。从收入结构看，山东省政府性基金预算收入主要集中于国有土地使用权出让收入；从管理角度看，土地出让收入相关收益主要集中于</p>
<p>市县级政府。考虑到上级补助收入、上年结余和调入资金等因素后，</p>
<p>2018-2020 年山东省政府性基金预算收入总计分别为 7927.99 亿元、</p>
<p>9283.65 亿元和 11520.85 亿元。</p>
<p>山东省政府性基金预算收入对土地的依赖程度较高，2018-2020 年全省国有土地使用权出让收入占政府性基金预算收入的比重分别为86.85%、90.27%和 91.36%。得益于土地市场行情的持续升温，2018-2020 年山东省国有土地使用权出让收入分别同比增长 66.0%、16.8%和 9.3%。</p>
</blockquote>
<p>2018-2020 年，山东省政府性基金预算支出分别完成 6707.79 亿元、</p>
<p>7532.22 亿元和 9783.62 亿元，主要为城乡社区支出。同期，山东省城</p>
<blockquote>
<p>乡社区支出分别完成 6436.68 亿元、7109.82 亿元和 6830.46 亿元，分别占当年全省政府性基金预算支出的 95.96%、94.39% 和 69.82% 。2018-2020 年，山东省政府性基金预算自给率4分别为 89.46%、89.52% 和 74.40%，基金预算收入对基金预算支出的保障程度处于相对较高水平。</p>
<p>4 政府性基金预算自给率=政府性基金预算收入/政府性基金预算支出*100%。</p>
<p>从省级政府性基金预算收支情况看，2018-2020 年山东省级政府性基金预算收入分别完成 72.05 亿元、86.62 亿元和 67.27 亿元，2020 年省级政府性基金预算收入同比下降 22.3%。2020 年省级政府性基金预算收入主要为国有土地使用权出让收入，占比为 59.50%。2018-2020 年， 山东省级政府性基金预算支出分别完成 71.15 亿元、107.04 亿元和</p>
<p>113.79 亿元。与收入结构相一致，2020 年省级政府性基金预算支出主要系国有土地使用权出让相关支出、彩票发行销售机构业务费安排的支出等。考虑专项债券收入、中央转移支付补助收入、市县上解收入及上年结转收入后，2018-2020 年山东省级政府性基金预算支出总计与收入总计实现平衡。</p>
<p>在政府性基金预算收支不考虑青岛市的情况下，2018-2020 年山东省（不含青岛）分别完成政府性基金预算收入 5115.10 亿元、5537.57</p>
<p>亿元和 6109.08 亿元；同期，山东省（不含青岛）政府性基金预算支出分别为 5782.21 亿元、6220.89 亿元和 8262.56，政府性基金预算自给率分别为 88.46%、89.02%和 73.94%。考虑到上解上级支出、调出资金及年终结余等因素后，2018-2020 年山东省（不含青岛）政府性基金预算支出总计和收入总计实现平衡。</p>
</blockquote>
<h3 id="山东省国有资本经营预算收支情况">3.山东省国有资本经营预算收支情况</h3>
<blockquote>
<p>山东省国有资本经营预算收入规模较小，2018-2020 年分别实现</p>
<p>57.34 亿元、79.65 亿元和 155.23 亿元，国有资本经营预算收入逐年增长，主要系利润收入增加所致。山东省国有资本经营预算收入主要以国有企业上缴利润收入、股利和股息收入以及产权转让收入为主， 2018-2020 年上述三项收入合计在国有资本经营预算收入中所占比重分别为 93.50%、89.47%和 91.96%。考虑到转移支付和上年结余因素后， 2018-2020 年，山东省国有资本经营预算收入总计分别为 70.78 亿元、</p>
<p>91.34 亿元和 167.11 亿元。</p>
<p>2018-2020 年，山东省国有资本经营预算支出分别完成 41.05 亿元、</p>
<p>45.29 亿元和 60.17 亿元。目前，解决历史遗留问题及改革成本支出、国有企业资本金注入支出是山东省国有资本经营预算支出的主要方向， 2020 年上述两项支出合计占全省国有资本经营预算支出中的比重为66.05%。考虑到上年结余、年终结余等因素后，2018-2020 年山东省国有资本经营预算支出总计和收入总计实现平衡。</p>
</blockquote>
<h2 id="三-山东省政府债务状况">（三） 山东省政府债务状况</h2>
<p>山东省政府债务规模较大，但较强的经济和财政实力能够为债务偿付提供较高保障，偿债压力相对较小。山东省财政资金的流动性较好， 对债务的管控措施较为完善，债务风险总体可控。</p>
<p>根据山东省财政厅提供的数据，截至 2020 年末山东省（含青岛）</p>
<p>政府债务余额为 16591.8 亿元，较 2019 年末增加 3464.3 亿元，其中一</p>
<blockquote>
<p>般债务余额为 7054.7 亿元，专项债务余额为 9537.1 亿元。从举债主体 所在地方政府层级来看（含青岛），2020 年末山东省级、市本级、县级 的债务比重分别为 8.26%、38.46%和 53.29%，债务分布情况较 2019 年末变化不大。从未来偿债年度看，山东省（含青岛）政府债务期限结构相对合理，其中 2021-2024 年到期需偿还的政府债务比重分别为 13.43%、9.86%、14.35%和 12.98%，2025 年及以后年度到期需偿还的政府债务比重为 49.38%。</p>
<p>山东省经济保持良好发展趋势，地区生产总值全国排名前列；全省一般公共预算收入在全国处于较高水平，财政收入持续平稳增长，可支配收入稳定性较高。山东省较强的经济发展水平和财政实力可为债务偿还提供有力保障。山东省政府不仅掌握着财政性货币资金，而且经营着政府性资产和土地、矿产、森林、岸线、航线等资源性资产。山东省政府资金、资产、资源的规范使用，及其在空间和时间上的配置合理性， 将提高资金、资产、资源的使用效率，有利于政府资金的调配和债务的及时偿付。同时，山东省政府拥有的优质资产有一定的增值空间，且可形成稳定的现金收益，为偿还债务提供进一步支撑。</p>
<p>政府债务管控方面，近年来山东省积极推进地方政府债务债券化改革，坚持融资发展和风险防范并重，多举措管好用好政府债务资金。2019 年 11 月，山东省财政厅等五部门印发《关于做好政府专项债券发行及</p>
<p>项目配套融资工作的实施意见》（鲁财债〔2019〕50 号），指导各级政府和部门积极推行“专项债券+市场化融资”组合融资模式；用好专项债券作为重大项目资本金政策；切实保障在建项目后续融资；合理提高长期专项债券比例；加强专项债券项目库管理；强化专项债券资金监管； 加快新增债券发行使用进度；全面推进债务信息公开。2020 年 8 月， 山东省财政厅和山东省发展和改革委员会印发《关于加快专项债券发行使用有关工作的紧急通知》（鲁财债〔2020〕47 号），指导各级政府和部门加快专项债券项目实施进度，抓紧做好债券发行工作，依法合规调整专项债券用途，强化负面清单管理，加快债券资金拨付使用进度，加强债券资金使用监管，严控专项债券风险。2020 年 11 月，山东省财政厅印发《山东省政府专项债券项目绩效管理暂行办法》（鲁财债〔2020〕70 号），指导各级政府和部门加强政府专项债券项目绩效管理，提高政府债券资金使用效益。</p>
<p>政府债务风险防范方面，山东省组织开展省级、市本级和县级债务风险指标测算，全面掌握各级债务风险状况；加强日常监控，完善债务统计报告制度，及时了解债务增减变化和风险状况，定期进行数据分析研究；拟订防范债务风险工作方案，排查债务风险点，健全化解债务风险措施。同时，山东省加强债务管理的考核监督，明确要求将债务收支全面纳入预算管理，不得超限额或在预算之外举借债务，不得以支持公益性事业发展名义举借债务用于经常性支出或楼堂馆所建设；将政府性债务率纳入对各市科学发展综合考核范围，依法加强对政府性债务的审计监督。</p>
<p>为进一步规范山东省各级政府举债融资行为，防范和化解地方政府性债务风险，山东省人民政府办公厅于 2017 年 9 月 30 日印发《山东省人民政府办公厅关于规范政府举债融资行为防控政府性债务风险的意见》（鲁政办字〔2017〕154 号）（简称“意见”），分别就防范化解地方政府性债务风险、控制新增政府性债务规模、化解存量政府性债务、规范政府和社会资本合作及政府购买服务行为、纠正违法违规举债融资担保行为、切实加强政府性债务信息公开、健全跨部门联合监管问责机制等方面，提出了具体的政策措施。意见中明确指出，全省力争用 2-3 年时间将限额内地方政府债务率控制在 100%的警戒线以内，用 3-5 年时间使隐性债务风险明显降低，全口径政府债务风险整体可控。2018 年11 月 11 日，山东省人民政府办公厅印发《山东省人民政府办公厅关于印发山东省政府性债务管理暂行办法的通知》（鲁政办字〔2018〕219</p>
<p>号），提出各级政府对本地区政府性债务实行统一领导、加强政府投资项目源头管控、政府债务余额实行限额管理、政府债务分类纳入全口径预算管理、划清政府债务与企业债务的界限、依法依规有序推进政府和社会资本合作、建立政府债务风险防控预警和应急处置机制、强化债务工作绩效考核等具体政策措施。</p>
</blockquote>
<h2 id="四-山东省政府治理状况">（四） 山东省政府治理状况</h2>
<p>山东省政府不断深化行政审批制度改革，负面清单制度初见成效， 政府运行效率与服务能力不断提升；政务信息披露及时，渠道丰富，信息透明度较高；山东省立足地区实际，制定了一系列重大且可行的地区经济、社会发展规划，政府战略管理能力较强。</p>
<blockquote>
<p>山东省政府不断深化行政审批制度改革，提高政府管理科学化水平， 政府运行效率与服务能力不断提升。2018 年，山东省取消下放省级行政权力事项 37 项，其中，取消 10 项、下放 27 项，涉及行政许可 26 项、</p>
<p>行政处罚 3 项、行政强制 1 项、行政确认 2 项、其他行政权力事项 4 项、</p>
<p>证明事项 1 项；2019 年，山东省取消省级行政权力事项 10 项，承接下</p>
<p>放管理层级行政权力事项 9 项；取消 4 项市级行政许可事项，承接下放</p>
<p>至市级实施的行政许可事项 1 项；取消 5 项县级行政许可事项，承接下</p>
<p>放至县级实施的行政许可事项 1 项。2020 年 3 月，山东省委、省政府发布《关于深化制度创新加快流程再造的指导意见》，提出大幅压减行政权力事项，3 年内将省级行政许可事项压减 50%以上。</p>
<p>同时，为进一步严肃财经纪律、维护财经秩序，更好地发挥财政专项资金使用效益，2019 年 12 月山东省发布《山东省人民政府关于印发山东省政府部门权责清单管理办法的通知》（鲁政字〔2019〕247 号）（简称“通知”），通知指出政府部门实施的行政许可、行政处罚、行政强制、行政征收、行政给付、行政裁决、行政确认、行政奖励、行政检查、其他行政权力等行政权力事项和公共服务事项及其对应的责任事项，以清单的形式列明，并向社会公开；政府部门应当按照现行法律、法规和规章等，结合“三定”规定，梳理权责事项，编制权责清单；政府部门应 当充分发挥权责清单制度的基础性制度效用，将权责清单贯穿到职能运行的各个环节各个方面，严格按照权责清单履职尽责，未纳入权责清单且无法定依据的权责事项不得实施；上级政府部门应当对下级政府部门落实权责清单制度情况进行指导和监督。</p>
<p>山东省政府信息透明度水平总体较好，能够根据《中华人民共和国</p>
<p>政府信息公开条例》、《山东省政府信息公开办法》等的规定，较及时地披露政务信息。2019 年，山东省继续将政府信息公开作为推进全面深化改革、全面依法治省，建设法治政府、阳光政府的重大举措，制发了</p>
<p>《山东省人民政府办公厅关于印发 2019 年山东省政务公开工作要点的通知》（鲁政办发〔2019〕15 号）等政策文件，进一步加大工作推动力度，全省政府信息公开步伐不断加快，公开实效明显提升。</p>
<p>山东省以加强管理服务、政策执行、民生领域、权力运行等方面信息公开为工作重点，切实保障人民群众知情权、参与权、表达权和监督权，助力深化改革、经济发展、民生改善和政府建设。2019 年，山东省各级政府和县级以上政府部门共收到政府信息公开申请 2.58 万件， 同比增长 17.9%。其中，山东省各级政府和县级以上政府部门答复政府信息公开申请 2.54 万件。未来，山东省政府将着力抓好制度机制的健全和落实工作，加强政府信息公开，做好监督检查和考核评估工作，进一步推进重点领域信息公开和相关政策解读，加强政策解读和社会关切回应工作，为建设法治政府、阳光政府做出积极贡献。</p>
<p>近年来，山东省政府在我国社会建设、经济发展、文化强国战略等的引导下，积极制定并稳步实施了《省会城市群经济圈发展规划》、《胶东经济圈一体化发展规划》、《中共山东省委关于制定山东省国民经济和社会发展第十三个五年规划的建议》以及《山东省新旧动能转换综合试验区建设总体方案》等一系列重要发展规划，为山东省经济发展和社会建设指明了方向。</p>
<p>在经济结构调整和转型升级方面，山东省积极实施新旧动能转换发展战略，加快淘汰落后动能、加快提升传统动能、加快培育新动能、加快增强创新能力、加快深化改革开放、加快释放市场活力。经过两年的努力，山东省新旧动能转换已经全面起势，正朝着“三年初见成效、五年取得突破、十年塑成优势”的下一阶段目标，加速向前迈进。具体来看，山东省治理“散乱污”企业超过 11 万家；钢铁、化工等产业重组迈出较大步伐，日照钢铁精品基地、烟台裕龙岛炼化一体化等项目顺利推进；省级大科学计划和大科学工程深入推进，山东产业技术研究院挂牌运营。未来，山东省仍将大力推进新一代信息技术、高端装备、新能源新材料、现代海洋、医养健康、高端化工、现代高效农业、文化创意、精品旅游、现代金融“十强”产业集群式发展；深入实施创新驱动发展 战略，优化创新资源配置，强化科技创新供给；聚焦关键环节和重点领域，强化有效制度供给；着力构建开放型经济发展新体制，释放新旧动</p>
<p>能转换潜力。</p>
<p>在体制建设方面，为适应国内外经济结构深刻调整、发展方式加快转变的新要求，山东省不断推进制度建设和体制创新，深化行政管理体制改革、财税体制改革、所有制结构改革和农村经济体制改革，充分发挥市场配置资源的基础性作用。2019 年 1 月，山东省第十一届委员会第八次全体会议通过进一步深化改革开放加快制度创新的决定（简称 “决定”），决定指出围绕加快推动新旧动能转换、打造乡村振兴齐鲁样板、建设现代化海洋强省等重点领域关键环节加快制度创新；注重制度创新的实施与操作，在实践中不断完善提升；健全制度创新责任体系， 强化制度创新督察考核。2020 年 1 月，山东省委、省政府印发了《贯彻落实&lt;中共中央国务院关于构建更加完善的要素市场化配置体制机制的意见&gt;的实施意见》（简称“意见”），意见聚焦土地、劳动力、资本、技术、数据 5 大要素，提出注重增强土地管理灵活性，着力畅通劳动力流动渠道，重视发挥好资本要素市场作用，进一步激发技术供给活力， 加快培育数据要素市场。</p>
<p>在扩大开放方面，山东省继续深化实施互利共赢的对外开放战略， 主动对接“一带一路”倡议，加强与“一带一路”倡议沿线国家经贸合 作与人文交流，进一步拓展全省在国际合作领域的广度和深度。2018 年 7 月，山东省人民政府办公厅印发《山东省深化与世界 500 强及行业领军企业合作行动方案（2018-2020 年）》（鲁政办字〔2018〕106 号），围绕深化合作内涵、完善招商机制、拓展招商渠道、增强园区承载力、优化营商环境、加大支持力度等方面提出具体措施。</p>
</blockquote>
<h2 id="五-外部支持">（五） 外部支持</h2>
<blockquote>
<p>山东省是中国（山东）自由贸易试验区（简称“山东省自贸试验区”）、中国——上海合作组织地方经贸合作示范区（简称“上合示范区”）以及山东新旧动能转换综合试验区（简称“新旧动能转换综合试验区”）“三区叠加”的重点开发区域，是环渤海经济圈、中原经济区以及京津冀一体化等国家级区域发展规划的重要交汇处。1992 年，党的十四大报告中提出要加快环渤海地区（即“环渤海经济圈”）的开发、开放，将这一地区列为全国开放开发的重点区域之一，目前环渤海地区已成为继珠江三角洲、长江三角洲之后的中国经济第三个“增长极”，山东省是环渤海地区重要的组成部分。2011 年，建设中原经济区上升为国家战略，中原经济区是国家重要的粮食生产和现代农业基地、全国“三化”协调发展</p>
<p>示范区、全国重要的经济增长板块、全国区域协调发展的战略支点和重要的现代综合交通枢纽、华夏历史文明传承创新区，其范围包含了山东省聊城市、菏泽市和泰安市东平县。2016 年 2 月，《“十三五”时期京津冀国民经济和社会发展规划》印发实施，这是全国第一个跨省市的区域“十三五”规划，明确了京津冀地区未来五年的发展目标，规划支持山东的聊城、德州、滨州、东营等周边毗邻地区融入京津冀协同发展国家战略，打造京津冀协同发展示范区。2018 年 1 月，国务院正式批复《山东新旧动能转换综合试验区建设总体方案》，同意设立新旧动能转换综合试验区，新旧动能转换综合试验区以新技术、新产业、新业态、新模式为核心，以知识、技术、信息、数据等新生产要素为支撑，积极探索新旧动能转换模式，为促进全国新旧动能转换、建设现代化经济体系作出积极贡献。2019 年 8 月，国务院印发《中国（山东）自由贸易试验区总体方案》，山东省自贸试验区旨在全面落实中央关于增强经济社会发展创新力、转变经济发展方式、建设海洋强国的要求，加快推进新旧发展动能接续转换、发展海洋经济，形成对外开放新高地。2019 年 9 月，国务院正式批复《中国—上海合作组织地方经贸合作示范区建设总体方案》，同意设立上合示范区，上合示范区旨在打造“一带一路”倡议， 拓展国际物流、现代贸易、双向投资、商旅文化交流等领域合作，着力推动形成陆海内外联动、东西双向互济的开放格局。受益于相关国家级战略，未来山东省发展面临良好机遇。</p>
</blockquote>
<h1 id="二本批债券信用质量分析">二、本批债券信用质量分析</h1>
<h2 id="一-主要条款">（一） 主要条款</h2>
<blockquote>
<p>2021 年山东省政府交通能源市政产业园基础设施及民生社会事业发展专项债券（一至四期）—2021 年山东省政府专项债券（一至四期） 计划发行总额为 119.29 亿元，品种为记账式固定利率附息债，债券期限分别为 10 年、20 年、30 年和 30 年（27+3 年，含权），计划发行规模分别为 30.25 亿元、38.39 亿元、45.65 亿元和 5.00 亿元。利息每半年支付一次，发行后可按规定在全国银行间债券市场和证券交易所债券市场上市流通。对于非含权债券，到期后一次性偿还本金并支付最后一次利息。对于 30 年（27+3 年，含权）债券，山东省财政厅有权于 2048</p>
<p>年 4 月 15 日前 30 日（节假日顺延），在中国债券信息网等公开渠道发</p>
<p>布是否行使赎回选择权的公告。若行使赎回权，则债券到期日为 2048</p>
<p>年 4 月 15 日（节假日顺延），到期还本并支付最后一次利息；若不行使</p>
<p>赎回权，则债券到期日为 2051 年 4 月 15 日（节假日顺延），到期还本并支付最后一次利息。</p>
</blockquote>
<h2 id="二-募集资金用途">（二） 募集资金用途</h2>
<blockquote>
<p>本批债券计划发行总额为 119.29 亿元，全部为新增债券。募集资金专项用于山东省省本级、济南市和滨州市交通能源市政产业园基础设施及民生社会事业发展项目。本批债券本息偿付资金主要来源于募投项目对应的运营收入。本批债券收入、支出、还本、付息等纳入山东省政府性基金预算管理，偿付保障程度高。</p>
</blockquote>
<h2 id="三-偿付保障分析">（三） 偿付保障分析</h2>
<h3 id="年山东省政府专项债券一期">1.2021 年山东省政府专项债券（一期）</h3>
<blockquote>
<p>本期债券涉及募投项目 40 个，债券期限为 10 年，本期债券收入、支出、还本、付息等纳入山东省政府性基金预算管理，偿付保障程度高。本期债券募投项目收入主要来源于学费、住宿费、住院收入、门诊收入、</p>
<p>供水收入、污水处理收入、土地出让收入等，总债务存续期5内募投项目可偿债收益能够覆盖总债务融资本息。本期债券拟募集资金 30.25 亿元， 用于青岛大学青大学生实习实训平台建设、烟台大学“双一流”建设项 目、山东科技大学实习实训基地建设项目、青岛科技大学 2021 年实训平</p>
<p>台建设项目等合计 40 个项目，项目预期可偿债收益总计 153.29 亿元， 各项目可偿债收益对总债务融资本息覆盖倍数6在 1.20 倍-3.54 倍之间。</p>
<p>5 总债务=专项债券融资+其他债务融资；总债务存续期指项目第一笔债务发生年度至项目最后一笔债务到期年度，下同。</p>
<p>6 覆盖倍数=项目可偿债收益/项目总债务融资本息，下同。</p>
</blockquote>
<h3 id="年山东省政府专项债券二期">2.2021 年山东省政府专项债券（二期）</h3>
<blockquote>
<p>本期债券涉及募投项目 26 个，债券期限为 20 年，本期债券收入、支出、还本、付息等纳入山东省政府性基金预算管理，偿付保障程度高。本期债券募投项目收入主要来源于学费、住宿费、培训收入、住院收入、物业租赁收入、污水处理收入、停车位收入等，总债务存续期内募投项目可偿债收益能够覆盖总债务融资本息。本期债券拟募集资金 38.39 亿元，用于山东科技职业学院双高计划建设项目、山东电子职业技术学院高水平专业群建设项目、青岛酒店管理职业技术学院高水平高职院校支持计划、山东交通职业学院综合交通运输公共实训基地等合计 26 个项目，</p>
<p>项目预期可偿债收益总计 436.06 亿元，各项目可偿债收益对总债务融资本息覆盖倍数在 1.20 倍-2.46 倍之间。</p>
</blockquote>
<h3 id="年山东省政府专项债券三期">3.2021 年山东省政府专项债券（三期）</h3>
<blockquote>
<p>本期债券涉及募投项目 7 个，债券期限为 30 年，本期债券收入、支出、还本、付息等纳入山东省政府性基金预算管理，偿付保障程度高。本期债券募投项目收入主要来源于铁路客运收入、托运收入、广告收入、住院收入、门诊收入、污水处理供水收入等，总债务存续期内募投项目可偿债收益能够覆盖总债务融资本息。本期债券拟募集资金 45.65 亿元， 用于新建潍坊至烟台铁路、新建莱西至荣成铁路、新建郑州至济南铁路濮阳至济南段、济南市槐荫人民医院急诊综合楼建设项目等合计 7 个项</p>
<p>目，项目预期可偿债收益总计 1467.39 亿元，各项目可偿债收益对总债务融资本息覆盖倍数在 1.20 倍-2.32 倍之间。</p>
</blockquote>
<h3 id="年山东省政府专项债券四期">4.2021 年山东省政府专项债券（四期）</h3>
<blockquote>
<p>本期债券募投项目为新建济南至莱芜高速铁路，债券期限为 30 年</p>
<p>（27+3 年，含权），本期债券收入、支出、还本、付息等纳入山东省政府性基金预算管理，偿付保障程度高。本期债券募投项目收入主要来源于铁路客运收入、托运收入、广告收入等，总债务存续期内募投项目可偿债收益能够覆盖总债务融资本息。本期债券拟募集资金 5.00 亿元，募</p>
<p>投项目预期可偿债收益总计 308.81 亿元，项目可偿债收益对总债务融资</p>
<p>本息覆盖倍数为 1.36 倍。</p>
</blockquote>
<h1 id="三结论">三、结论</h1>
<blockquote>
<p>近年来，山东省地区生产总值保持增长趋势，综合实力位居全国前列。作为工业和农业大省，山东省经济基础较好，产业竞争力较强；科技创新、丰富的人力资源和自然资源可为山东省经济发展提供较高保障； 但同时也持续面临着产业结构转型升级下的落后产能淘汰压力以及节 能环保压力。投资和消费是拉动全省经济增长的主要动力，近年来山东省投资结构持续优化。</p>
<p>山东省财政收入规模保持在较高水平，其中，可支配收入稳定性较高；一般公共预算收支自给能力较强，收支平衡对中央转移支付的依赖程度较小；国有土地使用权出让收入是政府性基金预算收入的主要组成部分，房地产市场和土地市场的波动对基金预算收入产生一定影响。</p>
<p>山东省政府债务规模较大，但较强的经济和财政实力能够为债务偿付提供较高保障，偿债压力相对较小。山东省财政资金的流动性较好， 对债务的管控措施较为完善，债务风险总体可控。</p>
<p>山东省政府不断深化行政审批制度改革，负面清单制度初见成效， 政府运行效率与服务能力不断提升；政务信息披露及时，渠道丰富，信息透明度较高；山东省立足地区实际，制定了一系列重大且可行的地区经济、社会发展规划，政府战略管理能力较强。</p>
<p>本批债券为新增债券，拟用于山东省交通能源市政产业园基础设施及民生社会事业发展项目，债券收入、支出、还本、付息等纳入山东省政府性基金预算管理，偿付保障程度高。从募投项目情况看，专项债券本息偿付资金主要来源于募投项目对应的运营收入，根据项目实施方案， 总债务存续期内募投项目可偿债收益能够覆盖总债务融资本息，但需关注未来项目建设进展、各项收入等不达预期对项目偿债资金流入的影响。</p>
</blockquote>
<h1 id="跟踪评级安排">跟踪评级安排</h1>
<blockquote>
<p>根据政府业务主管部门要求以及对地方债信用评级的指导意见，在本次评级的信用等级有效期至 2021 年山东省政府交通能源市政产业园基础设施及民生社会事业发展专项债券（一至四期）—2021 年山东省政府专项债券</p>
<p>（一至四期）的约定偿付日止内，本评级机构将对其进行持续跟踪评级，包括持续定期跟踪评级与不定期跟踪评级。</p>
<p>跟踪评级期间，本评级机构将持续关注山东省经济金融环境的变化、影响财政平衡能力的重大事件、山东省政府履行债务的情况等因素，并出具跟踪评级报告，以动态地反映山东省地方政府债券的信用状况。</p>
</blockquote>
<h2 id="一-跟踪评级时间和内容">（一） 跟踪评级时间和内容</h2>
<blockquote>
<p>本评级机构对本批债券的跟踪评级的期限为本评级报告出具日至失效</p>
<p>日。</p>
<p>定期跟踪评级将在本次信用评级报告出具后每 1 年出具一次正式的定期</p>
<p>跟踪评级报告。定期跟踪评级报告与首次评级报告保持衔接，如定期跟踪评级报告与上次评级报告在结论或重大事项出现差异的，本评级机构将作特别说明，并分析原因。</p>
<p>不定期跟踪评级自本次评级报告出具之日起进行。在发生可能影响本次评级报告结论的重大事项时，山东省政府应根据已作出的书面承诺及时告知本评级机构相应事项。本评级机构及评级人员将密切关注与山东省有关的信息，在认为必要时及时安排不定期跟踪评级并调整或维持原有信用级别。</p>
</blockquote>
<h2 id="二-跟踪评级程序">（二） 跟踪评级程序</h2>
<blockquote>
<p>跟踪评级将按照收集评级所需资料、现场调研、评级分析、评级委员会评审、出具评级报告、公告等程序进行。</p>
<p>本评级机构的跟踪评级报告和评级结果将对业务主管部门及业务主管部门要求的披露对象进行披露。</p>
<p>在持续跟踪评级报告出具之日后五个工作日内，山东省政府和本评级机构应在业务主管部门指定媒体及本评级机构的网站上公布持续跟踪评级结果。</p>
</blockquote>
<h1 id="附录一评级模型分析表及结果">附录一：评级模型分析表及结果</h1>
<h1 id="附录二评级结果释义">附录二：评级结果释义</h1>
<blockquote>
<p>根据财政部《关于做好 2015 年地方政府专项债券发行工作的通知》， 地方政府专项债券信用评级等级符号及含义如下：</p>
</blockquote>
</body>
</html>"""
    title = ["Main Title"]
    root = convert_html_string_with_xfix(html_string, title)
    json_obj = root.traverse()
    gold_obj = {
        "guid": "0",
        "label": NodeType.Root,
        "content": ["ROOT"],
        "children": [
            {
                "guid": "0.0",
                "label": NodeType.Heading,
                "content": ["Main Title"],
                "children": [
                    {
                        "guid": "0.0.0",
                        "label": NodeType.Heading,
                        "content": ["声明"],
                        "children": [
                            {
                                "guid": "0.0.0.0",
                                "label": NodeType.Text,
                                "content": [
                                    "本评级机构对 2021 年山东省政府交通能源市政产业园基础设施及民生社会事业发展专项债券（一至四期）—2021 年山东省政府专项债券（一至四期）的信用评级作如下声明："
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.1",
                                "label": NodeType.Text,
                                "content": [
                                    "本次债券信用评级的评级结论是本评级机构以及评级分析员在履行尽职调查基础上，根据本评级机构的地方政府债券信用评级标准和程序做出的独立判断。本次评级所依据的评级方法是新世纪评级《中国地方政府专项债券信用评级方法》。上述评级方法可于新世纪评级官方网站查询。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.2",
                                "label": NodeType.Text,
                                "content": [
                                    "本评级机构及本次地方政府债券信用评级分析员与债务人之间不存在除本次信用评级事项委托关系以外的任何影响评级行为独立、客观、公正的关联关系，并在信用评级过程中恪守诚信原则，保证出具的评级报告客观、公正、准确、及时。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.3",
                                "label": NodeType.Text,
                                "content": [
                                    "本评级机构的信用评级和其后的跟踪评级均依据地方政府所提供的资料，地方政府对其提供资料的合法性、真实性、完整性、准确性负责。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.4",
                                "label": NodeType.Text,
                                "content": [
                                    "鉴于信用评级的及时性，本评级机构将对地方政府债券进行跟踪评级。在信用等级有效期限内，地方政府在财政、地方经济外部经营环境等发生重大变化时应及时向本评级机构提供相关资料，本评级机构将按照相关评级业务规范，进行后续跟踪评级，并保留变更及公告信用等级的权利。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.5",
                                "label": NodeType.Text,
                                "content": [
                                    "本次地方政府债券信用评级结论不是引导投资者买卖或者持有地方政府发行的各类金融产品，以及债权人向地方政府授信、放贷或赊销的建议， 也不是对与地方政府相关金融产品或债务定价作出的相应评论。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.0.6",
                                "label": NodeType.Text,
                                "content": [
                                    "本评级报告所涉及的有关内容及数字分析均属敏感性商业资料，其版权归本评级机构所有，未经授权不得修改、复制、转载、散发、出售或以任何方式外传。"
                                ],
                                "children": [],
                            },
                        ],
                    },
                    {
                        "guid": "0.0.1",
                        "label": NodeType.Heading,
                        "content": ["释义"],
                        "children": [
                            {
                                "guid": "0.0.1.0",
                                "label": NodeType.Text,
                                "content": ["新世纪评级，或本评级机构：上海新世纪资信评估投资服务有限公司"],
                                "children": [],
                            },
                            {
                                "guid": "0.0.1.1",
                                "label": NodeType.Text,
                                "content": [
                                    "本批债券：2021 年山东省政府交通能源市政产业园基础设施及民生社会事业发展专项债券（一至四期）—2021 年山东省政府专项债券（一至四期）"
                                ],
                                "children": [],
                            },
                        ],
                    },
                    {
                        "guid": "0.0.2",
                        "label": NodeType.Heading,
                        "content": ["一、山东省政府信用质量分析"],
                        "children": [
                            {
                                "guid": "0.0.2.0",
                                "label": NodeType.Heading,
                                "content": ["（一） 山东省经济实力"],
                                "children": [
                                    {
                                        "guid": "0.0.2.0.0",
                                        "label": NodeType.Text,
                                        "content": [
                                            "近年来，山东省地区生产总值保持增长趋势，综合实力位居全国前 列。作为工业和农业大省，山东省经济基础较好，产业竞争力较强；科技创新、丰富的人力资源和自然资源可为山东省经济发展提供较高保障； 但同时也持续面临着产业结构转型升级下的落后产能淘汰压力以及节 能环保压力。投资和消费是拉动全省经济增长的主要动力，近年来山东省投资结构和消费结构持续优化。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.0.1",
                                        "label": NodeType.Text,
                                        "content": [
                                            "山东省地处我国胶东半岛，位于渤海、黄海之间，黄河横贯东西， 大运河纵穿南北，是我国重要的工业、农业和人口大省。全省土地面积"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.0.2",
                                        "label": NodeType.Text,
                                        "content": [
                                            "15.8 万平方公里，占全国的 1.6%。行政区划方面，截至 2020 年末，山东省下辖济南市、青岛市两个副省级市，以及淄博市、枣庄市、东营市、烟台市、潍坊市、济宁市、泰安市、威海市、日照市、临沂市、德州市、聊城市、滨州市和菏泽市十四个地级市。2019 年末，全省常住人口 1.01 亿人，占全国总人口的 7.19%。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.0.3",
                                        "label": NodeType.Text,
                                        "content": [
                                            "依托区位优势及丰富的劳动力资源等，山东省产业基础稳固，近年全省经济发展水平维持在全国先地位，但受新旧动能转换、去产能、环保趋严、新冠肺炎疫情冲击等因素影响，经济增速逐年下滑。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.0.4",
                                        "label": NodeType.Text,
                                        "content": [
                                            "2018-2020 年，山东省分别实现地区生产总值 6.66 万亿元、7.11 万亿元和 7.31 万亿元，按可比价格计算，分别比上年增长 6.3%、5.5%和 3.6%。从三次产业结构看，2020 年山东省第一产业增加值为 0.54 万亿元，同比增长 2.7%；第二产业增加值为 2.86 万亿元，同比增长 3.3%；第三产业增加值为 3.92 万亿元，同比增长 3.9%。2020 年，山东省三次产业结构比例由上年的 7.2：39.8：53.0 调整为 7.3：39.1：53.6。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.0.5",
                                        "label": NodeType.Text,
                                        "content": [
                                            "山东省拥有天然的地理区位优势和资源禀赋，已发现矿产种类 148 种，其中黄金、石油、铁矿石、煤炭、菱镁矿等矿产资源基础储量丰富， 全国排名前列。山东省近海海域占渤海和黄海总面积的 37%，滩涂面积占全国的 15%，是国内水产品和原盐的主产地之一。依靠优越的地理位置和丰富的自然资源，山东省长期以来一直是我国重要的农业大省，地区主要产品原盐、水产品、原油、棉花、油料等产量占全国的比重均处于较高水平。2020 年山东省农林牧渔业总产值为 1.02 万亿元，同比增长 3.0%，成为全国首个农业总产值过万亿元的省份；粮食总产量 5446.8 万吨，同比增长 1.7%，占全国粮食产量的 8.1%；当年，水产品总产量为 790.2 万吨，占全国水产品总产量的 12.1%，其中海水产品产量 679.5 万吨。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.0.6",
                                        "label": NodeType.Text,
                                        "content": [
                                            "山东省制造业基础较好，工业体量持续位居全国前列，但全省工业结构仍以重工业和传统行业为主，行业发展处于价值链中低端，面临较大环境保护、技术升级转型等压力。在此背景下，近年来全省持续推动新旧动能转换工程，化解钢铁、煤炭、电解铝、火电、建材等高耗能行业过剩产能，不断培育以新一代信息技术、高端装备、新能源新材料、现代海洋、医养健康等行业为主的新动能，目前动能转换已初见成效， 业经济增速整体有所提升。2020 年，山东省工业增加值为 2.31 万亿"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.0.7",
                                        "label": NodeType.Text,
                                        "content": [
                                            "元，同比增长 3.6%，增速较上年提高 1.5 个百分点。从新旧动能转换看， 2020 年全省压减焦化产能 729 万吨，退出地炼产能 1176 万吨；高新技术产业产值占规模以上工业产值比重为 45.1%，较上年提高 5.0 个百分点；新一代信息技术制造业、新能源新材料、高端装备等十强产业增加值分别增长 14.5%、19.6%和 9.0%，依次高于规模以上工业增加值增速"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.0.8",
                                        "label": NodeType.Text,
                                        "content": [
                                            "9.5 个、14.6 个和 4.0 个百分点；光电子器件、服务器、半导体分立器件、碳纤维、工业机器人等高端智能产品产量分别增长 24.8%、35.3%、15.5%、129.5%和 24.9%。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.0.9",
                                        "label": NodeType.Text,
                                        "content": [
                                            "服务业方面，近年来山东省服务业保持较快发展态势，服务业主导型经济结构进一步巩固。2020 年山东省服务业实现增加值3.92 万亿元， 占全省生产总值比重为 53.6%，较上年提高 0.8 个百分点；对经济增长的贡献率为 55.1%。同时，山东省持续推动服务业转型与发展，服务业新动能增势强劲。2020 年山东省规模以上服务业营业收入增长 3.5%， 其中，高技术服务业营业收入增长 11.5%。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.0.10",
                                        "label": NodeType.Text,
                                        "content": [
                                            "经济发展驱动力方面，投资和消费是拉动经济增长的主要动力，近年来山东省投资结构和消费结构持续优化。投资方面，2020 年山东省固定资产投资同比增长 3.6%，三次产业投资结构为 2.3：31.3：66.4。在重点投资领域中，2020 年山东省制造业投资增长 7.6%，对全部投资增长贡献率为 51.9%；高技术产业投资增长 21.6%，其中高技术制造业和服务业投资分别增长 38.1%和 8.4%。消费方面，2020 年山东省社会消费品零售总额 2.92 万亿元，较上年基本持平。从消费结构看，2020"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.0.11",
                                        "label": NodeType.Text,
                                        "content": [
                                            "年山东省智能家电和音像器材、新能源汽车较上年分别增长 1.6 倍和49.1%，能效等级 1、2 级家电商品增长 80.8%。从消费方式看，2020 年山东省实现网上零售额 4613.3 亿元，较上年增长 13.8%。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.0.12",
                                        "label": NodeType.Text,
                                        "content": [
                                            "作为我国最早开放的十四个沿海省份之一，山东省也是我国对外贸易的重要口岸之一，但近年来受全球经济变化和国内供需变动等因素影响，全省对外贸易情况有所波动。2020 年山东省进出口总额 2.20 万亿元，同比增长 7.5%，其中出口额为 1.31 万亿元，同比增长 17.3%；进口额为 0.90 万亿元，同比下降 4.1%。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.0.13",
                                        "label": NodeType.Text,
                                        "content": [
                                            "区域发展方面，山东省有 7 个市为沿海城市，目前已形成山东半岛蓝色经济区、黄河三角洲高效生态经济区、省会城市经济圈以及西部经济隆起带的发展格局。从各经济区的发展规划看，山东半岛蓝色经济区要发展海洋经济；省会城市群经济圈主要依托省会城市优势带动周边地区发展；黄河三角洲高效生态经济区主要发展高效和循环经济；西部"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.0.14",
                                        "label": NodeType.Text,
                                        "content": [
                                            "经济隆起带主要致力于建设具有较强竞争力的特色产业基地1，使西部地区成为山东经济发展新引擎。四大经济区均依托自身优势，协调发展， 共同推动山东省产业结构转型和升级。此外，2018 年 1 月，国务院正式批复《山东新旧动能转换综合试验区建设总体方案》，同意设立山东新旧动能转换综合试验区，该区位于山东省全境，包括济南、青岛、烟台三大核心城市，十四个设区市的国家和省级经济技术开发区、高新技术产业开发区以及海关特殊监管区域，形成“三核引领、多点突破、融合互动”的新旧动能转换总体布局。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.0.15",
                                        "label": NodeType.Text,
                                        "content": [
                                            "未来，山东省将继续致力于经济结构调整，实施高端高质高效的产业发展战略，推动传统产业向中高端迈进，发展现代制造业和新兴服务业，经济结构有望进一步优化。第一产业方面，山东省将持续推进千亿斤粮食产能建设，实施“渤海粮仓”科技工程和耕地质量提升计划，努力实现粮食生产稳步增长和农业生产现代化。第二产业方面，山东省将加快信息技术与传统制造业跨界融合，培育智能制造、协同制造、绿色制造、增材制造等新业态，促进传统制造业转型升级；加大新兴产业领军企业引导力度，鼓励各区域发挥特色优势，增强高端制造业的整体竞争力；此外，山东省将加快园区升级，创建国家生态工业示范园区，培育创新型产业集群。第三产业方面，在加快发展技术含量和附加值高的金融、物流、节能环保、电子商务等现代服务业的基础上，适应社会消费结构转型升级趋势，加快发展满足个性化、多样化消费需求的新兴服务业，支持发展健康服务业，树立“大旅游”理念，推动旅游产品标准化建设和定制化服务。"
                                        ],
                                        "children": [],
                                    },
                                ],
                            },
                            {
                                "guid": "0.0.2.1",
                                "label": NodeType.Heading,
                                "content": ["（二） 山东省财政实力"],
                                "children": [
                                    {
                                        "guid": "0.0.2.1.0",
                                        "label": NodeType.Text,
                                        "content": [
                                            "山东省财政收入规模保持在较高水平，其中，可支配收入稳定性较高；一般公共预算收支自给能力较强，收支平衡对中央转移支付的依赖程度较小；国有土地使用权出让收入是政府性基金预算收入的主要组成部分，房地产市场和土地市场情况对基金预算收入产生一定影响。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.1.1",
                                        "label": NodeType.Text,
                                        "content": [
                                            "2018-2020 年，山东省分别实现可支配收入21.99 万亿元、2.18 万亿元和 2.51 万亿元，受益于较大规模国有土地使用权出让相关收入实现， 全省可支配收入持续增长。山东省可支配收入主要来源于一般公共预算"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.1.2",
                                        "label": NodeType.Text,
                                        "content": ["收入总计，同期一般公共预算收入总计占可支配收入的比重分别为"],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.1.3",
                                        "label": NodeType.Text,
                                        "content": ["59.83%、56.99%和 53.50%。"],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.1.4",
                                        "label": NodeType.Heading,
                                        "content": ["1.山东省一般公共预算收支情况"],
                                        "children": [
                                            {
                                                "guid": "0.0.2.1.4.0",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "与经济发展水平相适应，山东省一般公共预算收入在全国处于较高水平，且近年来保持增长态势。2018-2020 年，山东省分别完成一般公共预算收入 6485.40 亿元、6526.71 亿元和 6559.90 亿元，同比分别增长6.3%、0.6%和 0.5%，受经济下行压力加大、实施更大规模减税降费以及新冠肺炎疫情冲击等因素影响，2019 年以来一般公共预算收入增速有所下降。考虑到上级补助收入、上年结余、债务收入及调入资金等因素后，2018-2020 年山东省一般公共预算收入总计分别为 11911.68 亿元、 12419.98 亿元和 13447.20 亿元。"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.4.1",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "从一般公共预算收入结构看，山东省一般公共预算收入以税收收入为主，2018-2020 年税收比率分别为 75.52%、74.30%和 72.53%，处于较高水平。2018-2020 年，山东省分别完成税收收入 4897.92 亿元、4849.29 亿元和 4757.59 亿元，同比分别增长 10.8%、-1.0%和-1.9%，2019年以来税收收入增速持续为负，主要系受全省落实减税降费以及新冠肺炎疫情冲击等因素影响。从税收结构看，山东省税种以增值税和所得税为主，2020 年增值税和企业所得税分别为 1814.47 亿元和 686.52 亿元，占当年税收收入的比重分别为 38.14%和 14.43%。"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.4.2",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "2018-2020 年，山东省非税收入分别完成 1587.47 亿元、1677.42 亿和 1802.31 亿元，同比分别增长-5.5%、5.7%和 7.4%，主要受减费降税等因素影响，2018 年非税收入有所下滑。山东省非税收入以行政事业性收费收入、专项收入和国有资源（资产）有偿使用收入为主，2020"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.4.3",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "年以上三项合计实现收入 1412.01 亿元，合计占当年非税收入的 78.34%。"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.4.4",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "2018-2020 年，山东省一般公共预算支出分别完成 10100.96 亿元、10739.76 亿元和 11231.17 亿元，同比分别增长 9.1%、6.3%和 4.6%。山东省一般公共预算支出主要集中于教育、社会保障和就业、农林水、城乡社区、一般公共服务和卫生健康等领域，各项重点支出得到有效保障。2018-2020 年，以上 6 个领域支出合计分别为 7197.20 亿元、7721.02 亿元和 8213.47 亿元，占全省一般公共预算支出的比重分别为 71.25%、71.89% 和 73.13%。2018-2020 年全省一般公共预算自给率3分别为"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.4.5",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "64.21%、60.77%和 58.41%。考虑到上解上级支出、债券还本、调出资金及结转下年支出等因素后，2018-2020 年山东省一般公共预算支出总计与收入总计实现平衡。"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.4.6",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "3 一般公共预算自给率=一般公共预算收入/一般公共预算支出*100%，下同。"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.4.7",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "从省级一般公共预算收支情况看，2018-2020 年山东省级一般公共预算收入分别完成 236.20 亿元、235.53 亿元和 183.66 亿元，其中税收"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.4.8",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "收入分别为 129.56 亿元、117.99 亿元和 67.80 亿元，受减税降费以及新冠肺炎疫情冲击等因素影响，2019 年以来税收收入有所下降；同期， 非税收入分别为 106.64 亿元、117.54 亿元和 115.86 亿元。2018-2020 年， 山东省级一般公共预算支出分别完成 908.67 亿元、1075.84 亿元和1028.64 亿元，主要集中于教育、农林水、社会保障和就业等方面，省级一般公共预算收入对其一般公共预算支出覆盖程度较低。考虑上解上级支出、债券转贷支出及安排稳定调节基金等因素后，山东省省级一般公共预算支出总计与收入总计实现平衡。"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.4.9",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "青岛市于 1986 年 10 月获国务院批准成为计划单列市，并获得相当于省一级的经济管理权限，经济发展较好，财政实力较强。在一般公共预算收支不考虑青岛市的情况下，收入方面，2018-2020 年山东省（不含青岛）一般公共预算收入分别完成 5253.48 亿元、5284.97 亿元和5306.08 亿元。支出方面，2018-2020 年山东省（不含青岛）一般公共预"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.4.10",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "算支出分别完成 8541.18 亿元、9163.78 亿元和 9646.52 亿元，一般公共预算自给率分别为 61.51%、57.67%和 55.01%。考虑到上级补助收入、上年结余、上解上级支出、结转下年支出等因素后，2018-2020 年山东省（不含青岛）一般公共预算收入和支出总计实现平衡。"
                                                ],
                                                "children": [],
                                            },
                                        ],
                                    },
                                    {
                                        "guid": "0.0.2.1.5",
                                        "label": NodeType.Heading,
                                        "content": ["2.山东省政府性基金预算收支情况"],
                                        "children": [
                                            {
                                                "guid": "0.0.2.1.5.0",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "2018-2020 年，山东省政府性基金预算收入分别完成 6000.62 亿元、"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.5.1",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "6742.71 亿元和 7278.99 亿元，同比分别增长 59.2%、12.4%和 8.0%，其"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.5.2",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "中 2018 年政府性基金收入大幅增加，主要系国有土地使用权出让相关收入、国有土地收益基金相关收入和城市基础设施配套费收入等大幅增加所致。从收入结构看，山东省政府性基金预算收入主要集中于国有土地使用权出让收入；从管理角度看，土地出让收入相关收益主要集中于"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.5.3",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "市县级政府。考虑到上级补助收入、上年结余和调入资金等因素后，"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.5.4",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "2018-2020 年山东省政府性基金预算收入总计分别为 7927.99 亿元、"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.5.5",
                                                "label": NodeType.Text,
                                                "content": ["9283.65 亿元和 11520.85 亿元。"],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.5.6",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "山东省政府性基金预算收入对土地的依赖程度较高，2018-2020 年全省国有土地使用权出让收入占政府性基金预算收入的比重分别为86.85%、90.27%和 91.36%。得益于土地市场行情的持续升温，2018-2020 年山东省国有土地使用权出让收入分别同比增长 66.0%、16.8%和 9.3%。"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.5.7",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "2018-2020 年，山东省政府性基金预算支出分别完成 6707.79 亿元、"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.5.8",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "7532.22 亿元和 9783.62 亿元，主要为城乡社区支出。同期，山东省城"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.5.9",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "乡社区支出分别完成 6436.68 亿元、7109.82 亿元和 6830.46 亿元，分别占当年全省政府性基金预算支出的 95.96%、94.39% 和 69.82% 。2018-2020 年，山东省政府性基金预算自给率4分别为 89.46%、89.52% 和 74.40%，基金预算收入对基金预算支出的保障程度处于相对较高水平。"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.5.10",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "4 政府性基金预算自给率=政府性基金预算收入/政府性基金预算支出*100%。"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.5.11",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "从省级政府性基金预算收支情况看，2018-2020 年山东省级政府性基金预算收入分别完成 72.05 亿元、86.62 亿元和 67.27 亿元，2020 年省级政府性基金预算收入同比下降 22.3%。2020 年省级政府性基金预算收入主要为国有土地使用权出让收入，占比为 59.50%。2018-2020 年， 山东省级政府性基金预算支出分别完成 71.15 亿元、107.04 亿元和"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.5.12",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "113.79 亿元。与收入结构相一致，2020 年省级政府性基金预算支出主要系国有土地使用权出让相关支出、彩票发行销售机构业务费安排的支出等。考虑专项债券收入、中央转移支付补助收入、市县上解收入及上年结转收入后，2018-2020 年山东省级政府性基金预算支出总计与收入总计实现平衡。"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.5.13",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "在政府性基金预算收支不考虑青岛市的情况下，2018-2020 年山东省（不含青岛）分别完成政府性基金预算收入 5115.10 亿元、5537.57"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.5.14",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "亿元和 6109.08 亿元；同期，山东省（不含青岛）政府性基金预算支出分别为 5782.21 亿元、6220.89 亿元和 8262.56，政府性基金预算自给率分别为 88.46%、89.02%和 73.94%。考虑到上解上级支出、调出资金及年终结余等因素后，2018-2020 年山东省（不含青岛）政府性基金预算支出总计和收入总计实现平衡。"
                                                ],
                                                "children": [],
                                            },
                                        ],
                                    },
                                    {
                                        "guid": "0.0.2.1.6",
                                        "label": NodeType.Heading,
                                        "content": ["3.山东省国有资本经营预算收支情况"],
                                        "children": [
                                            {
                                                "guid": "0.0.2.1.6.0",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "山东省国有资本经营预算收入规模较小，2018-2020 年分别实现"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.6.1",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "57.34 亿元、79.65 亿元和 155.23 亿元，国有资本经营预算收入逐年增长，主要系利润收入增加所致。山东省国有资本经营预算收入主要以国有企业上缴利润收入、股利和股息收入以及产权转让收入为主， 2018-2020 年上述三项收入合计在国有资本经营预算收入中所占比重分别为 93.50%、89.47%和 91.96%。考虑到转移支付和上年结余因素后， 2018-2020 年，山东省国有资本经营预算收入总计分别为 70.78 亿元、"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.6.2",
                                                "label": NodeType.Text,
                                                "content": ["91.34 亿元和 167.11 亿元。"],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.6.3",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "2018-2020 年，山东省国有资本经营预算支出分别完成 41.05 亿元、"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.2.1.6.4",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "45.29 亿元和 60.17 亿元。目前，解决历史遗留问题及改革成本支出、国有企业资本金注入支出是山东省国有资本经营预算支出的主要方向， 2020 年上述两项支出合计占全省国有资本经营预算支出中的比重为66.05%。考虑到上年结余、年终结余等因素后，2018-2020 年山东省国有资本经营预算支出总计和收入总计实现平衡。"
                                                ],
                                                "children": [],
                                            },
                                        ],
                                    },
                                ],
                            },
                            {
                                "guid": "0.0.2.2",
                                "label": NodeType.Heading,
                                "content": ["（三） 山东省政府债务状况"],
                                "children": [
                                    {
                                        "guid": "0.0.2.2.0",
                                        "label": NodeType.Text,
                                        "content": [
                                            "山东省政府债务规模较大，但较强的经济和财政实力能够为债务偿付提供较高保障，偿债压力相对较小。山东省财政资金的流动性较好， 对债务的管控措施较为完善，债务风险总体可控。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.2.1",
                                        "label": NodeType.Text,
                                        "content": ["根据山东省财政厅提供的数据，截至 2020 年末山东省（含青岛）"],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.2.2",
                                        "label": NodeType.Text,
                                        "content": [
                                            "政府债务余额为 16591.8 亿元，较 2019 年末增加 3464.3 亿元，其中一"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.2.3",
                                        "label": NodeType.Text,
                                        "content": [
                                            "般债务余额为 7054.7 亿元，专项债务余额为 9537.1 亿元。从举债主体 所在地方政府层级来看（含青岛），2020 年末山东省级、市本级、县级 的债务比重分别为 8.26%、38.46%和 53.29%，债务分布情况较 2019 年末变化不大。从未来偿债年度看，山东省（含青岛）政府债务期限结构相对合理，其中 2021-2024 年到期需偿还的政府债务比重分别为 13.43%、9.86%、14.35%和 12.98%，2025 年及以后年度到期需偿还的政府债务比重为 49.38%。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.2.4",
                                        "label": NodeType.Text,
                                        "content": [
                                            "山东省经济保持良好发展趋势，地区生产总值全国排名前列；全省一般公共预算收入在全国处于较高水平，财政收入持续平稳增长，可支配收入稳定性较高。山东省较强的经济发展水平和财政实力可为债务偿还提供有力保障。山东省政府不仅掌握着财政性货币资金，而且经营着政府性资产和土地、矿产、森林、岸线、航线等资源性资产。山东省政府资金、资产、资源的规范使用，及其在空间和时间上的配置合理性， 将提高资金、资产、资源的使用效率，有利于政府资金的调配和债务的及时偿付。同时，山东省政府拥有的优质资产有一定的增值空间，且可形成稳定的现金收益，为偿还债务提供进一步支撑。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.2.5",
                                        "label": NodeType.Text,
                                        "content": [
                                            "政府债务管控方面，近年来山东省积极推进地方政府债务债券化改革，坚持融资发展和风险防范并重，多举措管好用好政府债务资金。2019 年 11 月，山东省财政厅等五部门印发《关于做好政府专项债券发行及"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.2.6",
                                        "label": NodeType.Text,
                                        "content": [
                                            "项目配套融资工作的实施意见》（鲁财债〔2019〕50 号），指导各级政府和部门积极推行“专项债券+市场化融资”组合融资模式；用好专项债券作为重大项目资本金政策；切实保障在建项目后续融资；合理提高长期专项债券比例；加强专项债券项目库管理；强化专项债券资金监管； 加快新增债券发行使用进度；全面推进债务信息公开。2020 年 8 月， 山东省财政厅和山东省发展和改革委员会印发《关于加快专项债券发行使用有关工作的紧急通知》（鲁财债〔2020〕47 号），指导各级政府和部门加快专项债券项目实施进度，抓紧做好债券发行工作，依法合规调整专项债券用途，强化负面清单管理，加快债券资金拨付使用进度，加强债券资金使用监管，严控专项债券风险。2020 年 11 月，山东省财政厅印发《山东省政府专项债券项目绩效管理暂行办法》（鲁财债〔2020〕70 号），指导各级政府和部门加强政府专项债券项目绩效管理，提高政府债券资金使用效益。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.2.7",
                                        "label": NodeType.Text,
                                        "content": [
                                            "政府债务风险防范方面，山东省组织开展省级、市本级和县级债务风险指标测算，全面掌握各级债务风险状况；加强日常监控，完善债务统计报告制度，及时了解债务增减变化和风险状况，定期进行数据分析研究；拟订防范债务风险工作方案，排查债务风险点，健全化解债务风险措施。同时，山东省加强债务管理的考核监督，明确要求将债务收支全面纳入预算管理，不得超限额或在预算之外举借债务，不得以支持公益性事业发展名义举借债务用于经常性支出或楼堂馆所建设；将政府性债务率纳入对各市科学发展综合考核范围，依法加强对政府性债务的审计监督。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.2.8",
                                        "label": NodeType.Text,
                                        "content": [
                                            "为进一步规范山东省各级政府举债融资行为，防范和化解地方政府性债务风险，山东省人民政府办公厅于 2017 年 9 月 30 日印发《山东省人民政府办公厅关于规范政府举债融资行为防控政府性债务风险的意见》（鲁政办字〔2017〕154 号）（简称“意见”），分别就防范化解地方政府性债务风险、控制新增政府性债务规模、化解存量政府性债务、规范政府和社会资本合作及政府购买服务行为、纠正违法违规举债融资担保行为、切实加强政府性债务信息公开、健全跨部门联合监管问责机制等方面，提出了具体的政策措施。意见中明确指出，全省力争用 2-3 年时间将限额内地方政府债务率控制在 100%的警戒线以内，用 3-5 年时间使隐性债务风险明显降低，全口径政府债务风险整体可控。2018 年11 月 11 日，山东省人民政府办公厅印发《山东省人民政府办公厅关于印发山东省政府性债务管理暂行办法的通知》（鲁政办字〔2018〕219"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.2.9",
                                        "label": NodeType.Text,
                                        "content": [
                                            "号），提出各级政府对本地区政府性债务实行统一领导、加强政府投资项目源头管控、政府债务余额实行限额管理、政府债务分类纳入全口径预算管理、划清政府债务与企业债务的界限、依法依规有序推进政府和社会资本合作、建立政府债务风险防控预警和应急处置机制、强化债务工作绩效考核等具体政策措施。"
                                        ],
                                        "children": [],
                                    },
                                ],
                            },
                            {
                                "guid": "0.0.2.3",
                                "label": NodeType.Heading,
                                "content": ["（四） 山东省政府治理状况"],
                                "children": [
                                    {
                                        "guid": "0.0.2.3.0",
                                        "label": NodeType.Text,
                                        "content": [
                                            "山东省政府不断深化行政审批制度改革，负面清单制度初见成效， 政府运行效率与服务能力不断提升；政务信息披露及时，渠道丰富，信息透明度较高；山东省立足地区实际，制定了一系列重大且可行的地区经济、社会发展规划，政府战略管理能力较强。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.3.1",
                                        "label": NodeType.Text,
                                        "content": [
                                            "山东省政府不断深化行政审批制度改革，提高政府管理科学化水平， 政府运行效率与服务能力不断提升。2018 年，山东省取消下放省级行政权力事项 37 项，其中，取消 10 项、下放 27 项，涉及行政许可 26 项、"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.3.2",
                                        "label": NodeType.Text,
                                        "content": [
                                            "行政处罚 3 项、行政强制 1 项、行政确认 2 项、其他行政权力事项 4 项、"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.3.3",
                                        "label": NodeType.Text,
                                        "content": [
                                            "证明事项 1 项；2019 年，山东省取消省级行政权力事项 10 项，承接下"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.3.4",
                                        "label": NodeType.Text,
                                        "content": [
                                            "放管理层级行政权力事项 9 项；取消 4 项市级行政许可事项，承接下放"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.3.5",
                                        "label": NodeType.Text,
                                        "content": [
                                            "至市级实施的行政许可事项 1 项；取消 5 项县级行政许可事项，承接下"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.3.6",
                                        "label": NodeType.Text,
                                        "content": [
                                            "放至县级实施的行政许可事项 1 项。2020 年 3 月，山东省委、省政府发布《关于深化制度创新加快流程再造的指导意见》，提出大幅压减行政权力事项，3 年内将省级行政许可事项压减 50%以上。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.3.7",
                                        "label": NodeType.Text,
                                        "content": [
                                            "同时，为进一步严肃财经纪律、维护财经秩序，更好地发挥财政专项资金使用效益，2019 年 12 月山东省发布《山东省人民政府关于印发山东省政府部门权责清单管理办法的通知》（鲁政字〔2019〕247 号）（简称“通知”），通知指出政府部门实施的行政许可、行政处罚、行政强制、行政征收、行政给付、行政裁决、行政确认、行政奖励、行政检查、其他行政权力等行政权力事项和公共服务事项及其对应的责任事项，以清单的形式列明，并向社会公开；政府部门应当按照现行法律、法规和规章等，结合“三定”规定，梳理权责事项，编制权责清单；政府部门应 当充分发挥权责清单制度的基础性制度效用，将权责清单贯穿到职能运行的各个环节各个方面，严格按照权责清单履职尽责，未纳入权责清单且无法定依据的权责事项不得实施；上级政府部门应当对下级政府部门落实权责清单制度情况进行指导和监督。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.3.8",
                                        "label": NodeType.Text,
                                        "content": ["山东省政府信息透明度水平总体较好，能够根据《中华人民共和国"],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.3.9",
                                        "label": NodeType.Text,
                                        "content": [
                                            "政府信息公开条例》、《山东省政府信息公开办法》等的规定，较及时地披露政务信息。2019 年，山东省继续将政府信息公开作为推进全面深化改革、全面依法治省，建设法治政府、阳光政府的重大举措，制发了"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.3.10",
                                        "label": NodeType.Text,
                                        "content": [
                                            "《山东省人民政府办公厅关于印发 2019 年山东省政务公开工作要点的通知》（鲁政办发〔2019〕15 号）等政策文件，进一步加大工作推动力度，全省政府信息公开步伐不断加快，公开实效明显提升。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.3.11",
                                        "label": NodeType.Text,
                                        "content": [
                                            "山东省以加强管理服务、政策执行、民生领域、权力运行等方面信息公开为工作重点，切实保障人民群众知情权、参与权、表达权和监督权，助力深化改革、经济发展、民生改善和政府建设。2019 年，山东省各级政府和县级以上政府部门共收到政府信息公开申请 2.58 万件， 同比增长 17.9%。其中，山东省各级政府和县级以上政府部门答复政府信息公开申请 2.54 万件。未来，山东省政府将着力抓好制度机制的健全和落实工作，加强政府信息公开，做好监督检查和考核评估工作，进一步推进重点领域信息公开和相关政策解读，加强政策解读和社会关切回应工作，为建设法治政府、阳光政府做出积极贡献。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.3.12",
                                        "label": NodeType.Text,
                                        "content": [
                                            "近年来，山东省政府在我国社会建设、经济发展、文化强国战略等的引导下，积极制定并稳步实施了《省会城市群经济圈发展规划》、《胶东经济圈一体化发展规划》、《中共山东省委关于制定山东省国民经济和社会发展第十三个五年规划的建议》以及《山东省新旧动能转换综合试验区建设总体方案》等一系列重要发展规划，为山东省经济发展和社会建设指明了方向。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.3.13",
                                        "label": NodeType.Text,
                                        "content": [
                                            "在经济结构调整和转型升级方面，山东省积极实施新旧动能转换发展战略，加快淘汰落后动能、加快提升传统动能、加快培育新动能、加快增强创新能力、加快深化改革开放、加快释放市场活力。经过两年的努力，山东省新旧动能转换已经全面起势，正朝着“三年初见成效、五年取得突破、十年塑成优势”的下一阶段目标，加速向前迈进。具体来看，山东省治理“散乱污”企业超过 11 万家；钢铁、化工等产业重组迈出较大步伐，日照钢铁精品基地、烟台裕龙岛炼化一体化等项目顺利推进；省级大科学计划和大科学工程深入推进，山东产业技术研究院挂牌运营。未来，山东省仍将大力推进新一代信息技术、高端装备、新能源新材料、现代海洋、医养健康、高端化工、现代高效农业、文化创意、精品旅游、现代金融“十强”产业集群式发展；深入实施创新驱动发展 战略，优化创新资源配置，强化科技创新供给；聚焦关键环节和重点领域，强化有效制度供给；着力构建开放型经济发展新体制，释放新旧动"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.3.14",
                                        "label": NodeType.Text,
                                        "content": ["能转换潜力。"],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.3.15",
                                        "label": NodeType.Text,
                                        "content": [
                                            "在体制建设方面，为适应国内外经济结构深刻调整、发展方式加快转变的新要求，山东省不断推进制度建设和体制创新，深化行政管理体制改革、财税体制改革、所有制结构改革和农村经济体制改革，充分发挥市场配置资源的基础性作用。2019 年 1 月，山东省第十一届委员会第八次全体会议通过进一步深化改革开放加快制度创新的决定（简称 “决定”），决定指出围绕加快推动新旧动能转换、打造乡村振兴齐鲁样板、建设现代化海洋强省等重点领域关键环节加快制度创新；注重制度创新的实施与操作，在实践中不断完善提升；健全制度创新责任体系， 强化制度创新督察考核。2020 年 1 月，山东省委、省政府印发了《贯彻落实<中共中央国务院关于构建更加完善的要素市场化配置体制机制的意见>的实施意见》（简称“意见”），意见聚焦土地、劳动力、资本、技术、数据 5 大要素，提出注重增强土地管理灵活性，着力畅通劳动力流动渠道，重视发挥好资本要素市场作用，进一步激发技术供给活力， 加快培育数据要素市场。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.3.16",
                                        "label": NodeType.Text,
                                        "content": [
                                            "在扩大开放方面，山东省继续深化实施互利共赢的对外开放战略， 主动对接“一带一路”倡议，加强与“一带一路”倡议沿线国家经贸合 作与人文交流，进一步拓展全省在国际合作领域的广度和深度。2018 年 7 月，山东省人民政府办公厅印发《山东省深化与世界 500 强及行业领军企业合作行动方案（2018-2020 年）》（鲁政办字〔2018〕106 号），围绕深化合作内涵、完善招商机制、拓展招商渠道、增强园区承载力、优化营商环境、加大支持力度等方面提出具体措施。"
                                        ],
                                        "children": [],
                                    },
                                ],
                            },
                            {
                                "guid": "0.0.2.4",
                                "label": NodeType.Heading,
                                "content": ["（五） 外部支持"],
                                "children": [
                                    {
                                        "guid": "0.0.2.4.0",
                                        "label": NodeType.Text,
                                        "content": [
                                            "山东省是中国（山东）自由贸易试验区（简称“山东省自贸试验区”）、中国——上海合作组织地方经贸合作示范区（简称“上合示范区”）以及山东新旧动能转换综合试验区（简称“新旧动能转换综合试验区”）“三区叠加”的重点开发区域，是环渤海经济圈、中原经济区以及京津冀一体化等国家级区域发展规划的重要交汇处。1992 年，党的十四大报告中提出要加快环渤海地区（即“环渤海经济圈”）的开发、开放，将这一地区列为全国开放开发的重点区域之一，目前环渤海地区已成为继珠江三角洲、长江三角洲之后的中国经济第三个“增长极”，山东省是环渤海地区重要的组成部分。2011 年，建设中原经济区上升为国家战略，中原经济区是国家重要的粮食生产和现代农业基地、全国“三化”协调发展"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.2.4.1",
                                        "label": NodeType.Text,
                                        "content": [
                                            "示范区、全国重要的经济增长板块、全国区域协调发展的战略支点和重要的现代综合交通枢纽、华夏历史文明传承创新区，其范围包含了山东省聊城市、菏泽市和泰安市东平县。2016 年 2 月，《“十三五”时期京津冀国民经济和社会发展规划》印发实施，这是全国第一个跨省市的区域“十三五”规划，明确了京津冀地区未来五年的发展目标，规划支持山东的聊城、德州、滨州、东营等周边毗邻地区融入京津冀协同发展国家战略，打造京津冀协同发展示范区。2018 年 1 月，国务院正式批复《山东新旧动能转换综合试验区建设总体方案》，同意设立新旧动能转换综合试验区，新旧动能转换综合试验区以新技术、新产业、新业态、新模式为核心，以知识、技术、信息、数据等新生产要素为支撑，积极探索新旧动能转换模式，为促进全国新旧动能转换、建设现代化经济体系作出积极贡献。2019 年 8 月，国务院印发《中国（山东）自由贸易试验区总体方案》，山东省自贸试验区旨在全面落实中央关于增强经济社会发展创新力、转变经济发展方式、建设海洋强国的要求，加快推进新旧发展动能接续转换、发展海洋经济，形成对外开放新高地。2019 年 9 月，国务院正式批复《中国—上海合作组织地方经贸合作示范区建设总体方案》，同意设立上合示范区，上合示范区旨在打造“一带一路”倡议， 拓展国际物流、现代贸易、双向投资、商旅文化交流等领域合作，着力推动形成陆海内外联动、东西双向互济的开放格局。受益于相关国家级战略，未来山东省发展面临良好机遇。"
                                        ],
                                        "children": [],
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "guid": "0.0.3",
                        "label": NodeType.Heading,
                        "content": ["二、本批债券信用质量分析"],
                        "children": [
                            {
                                "guid": "0.0.3.0",
                                "label": NodeType.Heading,
                                "content": ["（一） 主要条款"],
                                "children": [
                                    {
                                        "guid": "0.0.3.0.0",
                                        "label": NodeType.Text,
                                        "content": [
                                            "2021 年山东省政府交通能源市政产业园基础设施及民生社会事业发展专项债券（一至四期）—2021 年山东省政府专项债券（一至四期） 计划发行总额为 119.29 亿元，品种为记账式固定利率附息债，债券期限分别为 10 年、20 年、30 年和 30 年（27+3 年，含权），计划发行规模分别为 30.25 亿元、38.39 亿元、45.65 亿元和 5.00 亿元。利息每半年支付一次，发行后可按规定在全国银行间债券市场和证券交易所债券市场上市流通。对于非含权债券，到期后一次性偿还本金并支付最后一次利息。对于 30 年（27+3 年，含权）债券，山东省财政厅有权于 2048"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.3.0.1",
                                        "label": NodeType.Text,
                                        "content": [
                                            "年 4 月 15 日前 30 日（节假日顺延），在中国债券信息网等公开渠道发"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.3.0.2",
                                        "label": NodeType.Text,
                                        "content": [
                                            "布是否行使赎回选择权的公告。若行使赎回权，则债券到期日为 2048"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.3.0.3",
                                        "label": NodeType.Text,
                                        "content": [
                                            "年 4 月 15 日（节假日顺延），到期还本并支付最后一次利息；若不行使"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.3.0.4",
                                        "label": NodeType.Text,
                                        "content": [
                                            "赎回权，则债券到期日为 2051 年 4 月 15 日（节假日顺延），到期还本并支付最后一次利息。"
                                        ],
                                        "children": [],
                                    },
                                ],
                            },
                            {
                                "guid": "0.0.3.1",
                                "label": NodeType.Heading,
                                "content": ["（二） 募集资金用途"],
                                "children": [
                                    {
                                        "guid": "0.0.3.1.0",
                                        "label": NodeType.Text,
                                        "content": [
                                            "本批债券计划发行总额为 119.29 亿元，全部为新增债券。募集资金专项用于山东省省本级、济南市和滨州市交通能源市政产业园基础设施及民生社会事业发展项目。本批债券本息偿付资金主要来源于募投项目对应的运营收入。本批债券收入、支出、还本、付息等纳入山东省政府性基金预算管理，偿付保障程度高。"
                                        ],
                                        "children": [],
                                    }
                                ],
                            },
                            {
                                "guid": "0.0.3.2",
                                "label": NodeType.Heading,
                                "content": ["（三） 偿付保障分析"],
                                "children": [
                                    {
                                        "guid": "0.0.3.2.0",
                                        "label": NodeType.Heading,
                                        "content": ["1.2021 年山东省政府专项债券（一期）"],
                                        "children": [
                                            {
                                                "guid": "0.0.3.2.0.0",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "本期债券涉及募投项目 40 个，债券期限为 10 年，本期债券收入、支出、还本、付息等纳入山东省政府性基金预算管理，偿付保障程度高。本期债券募投项目收入主要来源于学费、住宿费、住院收入、门诊收入、"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.3.2.0.1",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "供水收入、污水处理收入、土地出让收入等，总债务存续期5内募投项目可偿债收益能够覆盖总债务融资本息。本期债券拟募集资金 30.25 亿元， 用于青岛大学青大学生实习实训平台建设、烟台大学“双一流”建设项 目、山东科技大学实习实训基地建设项目、青岛科技大学 2021 年实训平"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.3.2.0.2",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "台建设项目等合计 40 个项目，项目预期可偿债收益总计 153.29 亿元， 各项目可偿债收益对总债务融资本息覆盖倍数6在 1.20 倍-3.54 倍之间。"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.3.2.0.3",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "5 总债务=专项债券融资+其他债务融资；总债务存续期指项目第一笔债务发生年度至项目最后一笔债务到期年度，下同。"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.3.2.0.4",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "6 覆盖倍数=项目可偿债收益/项目总债务融资本息，下同。"
                                                ],
                                                "children": [],
                                            },
                                        ],
                                    },
                                    {
                                        "guid": "0.0.3.2.1",
                                        "label": NodeType.Heading,
                                        "content": ["2.2021 年山东省政府专项债券（二期）"],
                                        "children": [
                                            {
                                                "guid": "0.0.3.2.1.0",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "本期债券涉及募投项目 26 个，债券期限为 20 年，本期债券收入、支出、还本、付息等纳入山东省政府性基金预算管理，偿付保障程度高。本期债券募投项目收入主要来源于学费、住宿费、培训收入、住院收入、物业租赁收入、污水处理收入、停车位收入等，总债务存续期内募投项目可偿债收益能够覆盖总债务融资本息。本期债券拟募集资金 38.39 亿元，用于山东科技职业学院双高计划建设项目、山东电子职业技术学院高水平专业群建设项目、青岛酒店管理职业技术学院高水平高职院校支持计划、山东交通职业学院综合交通运输公共实训基地等合计 26 个项目，"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.3.2.1.1",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "项目预期可偿债收益总计 436.06 亿元，各项目可偿债收益对总债务融资本息覆盖倍数在 1.20 倍-2.46 倍之间。"
                                                ],
                                                "children": [],
                                            },
                                        ],
                                    },
                                    {
                                        "guid": "0.0.3.2.2",
                                        "label": NodeType.Heading,
                                        "content": ["3.2021 年山东省政府专项债券（三期）"],
                                        "children": [
                                            {
                                                "guid": "0.0.3.2.2.0",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "本期债券涉及募投项目 7 个，债券期限为 30 年，本期债券收入、支出、还本、付息等纳入山东省政府性基金预算管理，偿付保障程度高。本期债券募投项目收入主要来源于铁路客运收入、托运收入、广告收入、住院收入、门诊收入、污水处理供水收入等，总债务存续期内募投项目可偿债收益能够覆盖总债务融资本息。本期债券拟募集资金 45.65 亿元， 用于新建潍坊至烟台铁路、新建莱西至荣成铁路、新建郑州至济南铁路濮阳至济南段、济南市槐荫人民医院急诊综合楼建设项目等合计 7 个项"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.3.2.2.1",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "目，项目预期可偿债收益总计 1467.39 亿元，各项目可偿债收益对总债务融资本息覆盖倍数在 1.20 倍-2.32 倍之间。"
                                                ],
                                                "children": [],
                                            },
                                        ],
                                    },
                                    {
                                        "guid": "0.0.3.2.3",
                                        "label": NodeType.Heading,
                                        "content": ["4.2021 年山东省政府专项债券（四期）"],
                                        "children": [
                                            {
                                                "guid": "0.0.3.2.3.0",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "本期债券募投项目为新建济南至莱芜高速铁路，债券期限为 30 年"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.3.2.3.1",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "（27+3 年，含权），本期债券收入、支出、还本、付息等纳入山东省政府性基金预算管理，偿付保障程度高。本期债券募投项目收入主要来源于铁路客运收入、托运收入、广告收入等，总债务存续期内募投项目可偿债收益能够覆盖总债务融资本息。本期债券拟募集资金 5.00 亿元，募"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.3.2.3.2",
                                                "label": NodeType.Text,
                                                "content": [
                                                    "投项目预期可偿债收益总计 308.81 亿元，项目可偿债收益对总债务融资"
                                                ],
                                                "children": [],
                                            },
                                            {
                                                "guid": "0.0.3.2.3.3",
                                                "label": NodeType.Text,
                                                "content": ["本息覆盖倍数为 1.36 倍。"],
                                                "children": [],
                                            },
                                        ],
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "guid": "0.0.4",
                        "label": NodeType.Heading,
                        "content": ["三、结论"],
                        "children": [
                            {
                                "guid": "0.0.4.0",
                                "label": NodeType.Text,
                                "content": [
                                    "近年来，山东省地区生产总值保持增长趋势，综合实力位居全国前列。作为工业和农业大省，山东省经济基础较好，产业竞争力较强；科技创新、丰富的人力资源和自然资源可为山东省经济发展提供较高保障； 但同时也持续面临着产业结构转型升级下的落后产能淘汰压力以及节 能环保压力。投资和消费是拉动全省经济增长的主要动力，近年来山东省投资结构持续优化。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.4.1",
                                "label": NodeType.Text,
                                "content": [
                                    "山东省财政收入规模保持在较高水平，其中，可支配收入稳定性较高；一般公共预算收支自给能力较强，收支平衡对中央转移支付的依赖程度较小；国有土地使用权出让收入是政府性基金预算收入的主要组成部分，房地产市场和土地市场的波动对基金预算收入产生一定影响。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.4.2",
                                "label": NodeType.Text,
                                "content": [
                                    "山东省政府债务规模较大，但较强的经济和财政实力能够为债务偿付提供较高保障，偿债压力相对较小。山东省财政资金的流动性较好， 对债务的管控措施较为完善，债务风险总体可控。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.4.3",
                                "label": NodeType.Text,
                                "content": [
                                    "山东省政府不断深化行政审批制度改革，负面清单制度初见成效， 政府运行效率与服务能力不断提升；政务信息披露及时，渠道丰富，信息透明度较高；山东省立足地区实际，制定了一系列重大且可行的地区经济、社会发展规划，政府战略管理能力较强。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.4.4",
                                "label": NodeType.Text,
                                "content": [
                                    "本批债券为新增债券，拟用于山东省交通能源市政产业园基础设施及民生社会事业发展项目，债券收入、支出、还本、付息等纳入山东省政府性基金预算管理，偿付保障程度高。从募投项目情况看，专项债券本息偿付资金主要来源于募投项目对应的运营收入，根据项目实施方案， 总债务存续期内募投项目可偿债收益能够覆盖总债务融资本息，但需关注未来项目建设进展、各项收入等不达预期对项目偿债资金流入的影响。"
                                ],
                                "children": [],
                            },
                        ],
                    },
                    {
                        "guid": "0.0.5",
                        "label": NodeType.Heading,
                        "content": ["跟踪评级安排"],
                        "children": [
                            {
                                "guid": "0.0.5.0",
                                "label": NodeType.Text,
                                "content": [
                                    "根据政府业务主管部门要求以及对地方债信用评级的指导意见，在本次评级的信用等级有效期至 2021 年山东省政府交通能源市政产业园基础设施及民生社会事业发展专项债券（一至四期）—2021 年山东省政府专项债券"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.5.1",
                                "label": NodeType.Text,
                                "content": [
                                    "（一至四期）的约定偿付日止内，本评级机构将对其进行持续跟踪评级，包括持续定期跟踪评级与不定期跟踪评级。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.5.2",
                                "label": NodeType.Text,
                                "content": [
                                    "跟踪评级期间，本评级机构将持续关注山东省经济金融环境的变化、影响财政平衡能力的重大事件、山东省政府履行债务的情况等因素，并出具跟踪评级报告，以动态地反映山东省地方政府债券的信用状况。"
                                ],
                                "children": [],
                            },
                            {
                                "guid": "0.0.5.3",
                                "label": NodeType.Heading,
                                "content": ["（一） 跟踪评级时间和内容"],
                                "children": [
                                    {
                                        "guid": "0.0.5.3.0",
                                        "label": NodeType.Text,
                                        "content": ["本评级机构对本批债券的跟踪评级的期限为本评级报告出具日至失效"],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.5.3.1",
                                        "label": NodeType.Text,
                                        "content": ["日。"],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.5.3.2",
                                        "label": NodeType.Text,
                                        "content": [
                                            "定期跟踪评级将在本次信用评级报告出具后每 1 年出具一次正式的定期"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.5.3.3",
                                        "label": NodeType.Text,
                                        "content": [
                                            "跟踪评级报告。定期跟踪评级报告与首次评级报告保持衔接，如定期跟踪评级报告与上次评级报告在结论或重大事项出现差异的，本评级机构将作特别说明，并分析原因。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.5.3.4",
                                        "label": NodeType.Text,
                                        "content": [
                                            "不定期跟踪评级自本次评级报告出具之日起进行。在发生可能影响本次评级报告结论的重大事项时，山东省政府应根据已作出的书面承诺及时告知本评级机构相应事项。本评级机构及评级人员将密切关注与山东省有关的信息，在认为必要时及时安排不定期跟踪评级并调整或维持原有信用级别。"
                                        ],
                                        "children": [],
                                    },
                                ],
                            },
                            {
                                "guid": "0.0.5.4",
                                "label": NodeType.Heading,
                                "content": ["（二） 跟踪评级程序"],
                                "children": [
                                    {
                                        "guid": "0.0.5.4.0",
                                        "label": NodeType.Text,
                                        "content": [
                                            "跟踪评级将按照收集评级所需资料、现场调研、评级分析、评级委员会评审、出具评级报告、公告等程序进行。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.5.4.1",
                                        "label": NodeType.Text,
                                        "content": [
                                            "本评级机构的跟踪评级报告和评级结果将对业务主管部门及业务主管部门要求的披露对象进行披露。"
                                        ],
                                        "children": [],
                                    },
                                    {
                                        "guid": "0.0.5.4.2",
                                        "label": NodeType.Text,
                                        "content": [
                                            "在持续跟踪评级报告出具之日后五个工作日内，山东省政府和本评级机构应在业务主管部门指定媒体及本评级机构的网站上公布持续跟踪评级结果。"
                                        ],
                                        "children": [],
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "guid": "0.0.6",
                        "label": NodeType.Heading,
                        "content": ["附录一：评级模型分析表及结果"],
                        "children": [],
                    },
                    {
                        "guid": "0.0.7",
                        "label": NodeType.Heading,
                        "content": ["附录二：评级结果释义"],
                        "children": [
                            {
                                "guid": "0.0.7.0",
                                "label": NodeType.Text,
                                "content": [
                                    "根据财政部《关于做好 2015 年地方政府专项债券发行工作的通知》， 地方政府专项债券信用评级等级符号及含义如下："
                                ],
                                "children": [],
                            }
                        ],
                    },
                ],
            }
        ],
    }

    assert json_obj == gold_obj
    xx = json.dumps(json_obj, ensure_ascii=False)
    assert xx == json.dumps(gold_obj, ensure_ascii=False)


def test_convert_json_to_node():
    html_content = """
    <p>Text before heading 1</p>
    <h1>Heading 1</h1>
        <p>Text after heading 1</p>
        <h2>###Text1。</h2>
        <h2>###Text2。</h2>
        <h2>Heading 1.1</h2>
            <p>Text 3</p>
        <h2>###Text4。</h2>
        <h2>###Text5。</h2>
        <h2>Heading 1.2</h2>
            <p>Text 6</p>
            <p>Text 7</p>
        <h2>###Text8。</h2>
        <h2>###Text9。</h2>
    <h1>Heading 2</h1>
        <h2>###Text10。</h2>
        <h2>###Text11。</h2>
    """
    # 文档树
    html = etree.HTML(html_content)
    # 从excel中抽出来的大标题，可以是单行或多行的，但是必须得是list
    title = ["Main Title", "--Second Line Title"]
    node_list = convert_html_to_line_json(html)
    root_node = convert_to_universal_format(node_list, title, prefix="###", suffix="。")
    json_obj = root_node.traverse()
    root_node_recover = convert_json_to_node(json_obj)
    assert json_obj == root_node_recover.traverse()


if __name__ == "__main__":
    test_parse()
