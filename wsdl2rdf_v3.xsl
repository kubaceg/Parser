<?xml version="1.0" ?>

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
    xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
	xmlns:sawsdl="http://www.w3.org/ns/sawsdl"
	xmlns:inf="http://127.0.0.1/inference#"
	xmlns:xsdd="http://www.w3.org/2001/XMLSchema"
	xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
    >
  <xsl:output method="xml" indent="yes" media-type="application/rdf+xml" />
  <xsl:param name="filename"></xsl:param>
  <xsl:variable name="defaulturi">
    <xsl:text>http://127.0.0.1/</xsl:text>
  </xsl:variable>
  <xsl:variable name="baseuri">
    <xsl:value-of select="$defaulturi"/>
    <xsl:value-of select="$filename"/>
  </xsl:variable>

  <xsl:template match="wsdl:definitions">
    <rdf:RDF>
      <wsdl:definitions rdf:about="{$baseuri}#wsdl.definitions()">
        <xsl:apply-templates mode="message-inner" select="//wsdl:portType/wsdl:operation/*"/>
        <xsl:if test="@name">
          <inf:hasLabel rdf:resource="{$defaulturi}Label({@name})"/>
        </xsl:if>
      </wsdl:definitions>
      <xsl:apply-templates/>
    </rdf:RDF>
  </xsl:template>

  <xsl:template match="wsdl:message">
    <wsdl:message rdf:about="{$baseuri}#wsdl.message({@name})">
      <xsl:apply-templates mode="attribute-inner" select="@*"/>
      <xsl:apply-templates mode="message-inner" select="./wsdl:part"/>
    </wsdl:message>
    <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="wsdl:part" mode="message-inner">
    <inf:consistsOf rdf:resource="{$baseuri}#wsdl.part({../@name}/{@name})"/>
  </xsl:template>

  <xsl:template match="wsdl:part">
    <wsdl:part rdf:about="{$baseuri}#wsdl.part({../@name}/{@name})">
      <xsl:apply-templates mode="attribute-inner" select="@*"/>
    </wsdl:part>
  </xsl:template>

  <xsl:template match="wsdl:types/xsdd:schema">
    <xsl:apply-templates mode="types-inner" select="//xsdd:element | //xsdd:complexType | //xsdd:simpleType"/>
  </xsl:template>

  <xsl:template match="xsdd:simpleType" mode="types-inner">
    <xsl:if test="@name">
      <xsd:simpleType rdf:about="{$baseuri}#xsd.type({@name})">
        <xsl:apply-templates mode="complex-inner" select=".//xsdd:element"/>
        <xsl:apply-templates mode="attribute-inner" select="@*"/>
        <xsl:apply-templates mode="simple-inner" />
      </xsd:simpleType>
    </xsl:if>
  </xsl:template>

  <xsl:template match="xsdd:restriction" mode="simple-inner">
    <xsl:variable name="nss" select="substring-after(@base, ':')" />
    <xsl:variable name="nsletter" select="substring-before(@base, ':')"/>
    <xsl:variable name ="namespace" select="/*/namespace::*[name()=$nsletter]"/>
    <xsl:choose>
      <xsl:when test="$namespace='http://www.w3.org/2001/XMLSchema'">
        <inf:hasType rdf:resource="http://www.w3.org/2001/XMLSchema#{$nss}"/>
      </xsl:when>
      <xsl:otherwise>
        <inf:hasType rdf:resource="{$baseuri}#xsd.type({@base})"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="xsdd:element" mode="types-inner">
    <xsl:if test="@name">
      <xsd:element rdf:about="{$baseuri}#xsd.element({@name})">
        <xsl:apply-templates mode="complex-inner" select=".//xsdd:element"/>
        <xsl:apply-templates mode="attribute-inner" select="@*"/>
      </xsd:element>
    </xsl:if>
  </xsl:template>

  <xsl:template match="xsdd:complexType" mode="types-inner">
    <xsl:if test="@name">
      <xsd:complexType rdf:about="{$baseuri}#xsd.type({@name})">
        <xsl:apply-templates mode="attribute-inner" select="@*"/>
        <xsl:apply-templates mode="complex-inner" select=".//xsdd:element"/>
        <xsl:apply-templates mode="complex-inner" select=".//xsdd:attribute"/>
      </xsd:complexType>
    </xsl:if>
  </xsl:template>

  <xsl:template match="xsdd:element" mode="complex-inner">
    <inf:consistsOf rdf:resource="{$baseuri}#xsd.element({@name})"/>
  </xsl:template>

  <xsl:template match="xsdd:attribute" mode="complex-inner">
    <xsl:for-each select="@wsdl:arrayType">
      <xsl:variable name="iri">
        <xsl:call-template name="crop-iri"/>
      </xsl:variable>
      <xsl:variable name="irii" select="substring-before($iri, '[]')" />
      <inf:consistsOf rdf:resource="{$baseuri}#xsd.type({$irii})"/>
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="wsdl:output" mode="message-inner">
    <xsl:for-each select="@message">
      <xsl:variable name="iri">
        <xsl:call-template name="crop-iri"/>
      </xsl:variable>
      <inf:hasOutput rdf:resource="{$baseuri}#wsdl.message({$iri})"/>
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="wsdl:input" mode="message-inner">
    <xsl:for-each select="@message">
      <xsl:variable name="iri">
        <xsl:call-template name="crop-iri"/>
      </xsl:variable>
      <inf:hasInput rdf:resource="{$baseuri}#wsdl.message({$iri})"/>
    </xsl:for-each>
  </xsl:template>

  <xsl:template match="@type" mode="attribute-inner">
    <xsl:variable name="iri">
      <xsl:call-template name="crop-iri"/>
    </xsl:variable>
    <xsl:variable name="nsletter" select="substring-before(., ':')"/>
    <xsl:variable name ="namespace" select="/*/namespace::*[name()=$nsletter]"/>
    <xsl:choose>
      <xsl:when test="$namespace='http://www.w3.org/2001/XMLSchema'">
        <inf:hasType rdf:resource="http://www.w3.org/2001/XMLSchema#{$iri}"/>
      </xsl:when>
      <xsl:otherwise>
        <inf:hasType rdf:resource="{$baseuri}#xsd.type({$iri})"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="@name" mode="attribute-inner">
    <inf:hasLabel rdf:resource="{$defaulturi}Label({.})"/>
  </xsl:template>

  <xsl:template match="@element" mode="attribute-inner">
    <xsl:variable name="iri">
      <xsl:call-template name="crop-iri"/>
    </xsl:variable>
    <inf:consistsOf rdf:resource="{$baseuri}#xsd.element({$iri})"/>
  </xsl:template>

  <xsl:template match="@sawsdl:modelReference" mode="attribute-inner">
    <xsl:if test="string-length(.) &gt; 0">
      <inf:semanticAnnotation rdf:resource="{.}"/>
    </xsl:if>
  </xsl:template>

  <xsl:template name="crop-iri">
    <xsl:variable name="nss" select="substring-after(., ':')" />
    <xsl:choose>
      <xsl:when test="$nss">
        <xsl:value-of select="$nss"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="."/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="text()" mode="complex-inner"/>
  <xsl:template match="text()" mode="simple-inner"/>
  <xsl:template match="text()" mode="message-inner"/>
  <xsl:template match="@*" mode="attribute-inner"/>
  <xsl:template match="text()" mode="inner"/>
  <xsl:template match="text()" mode="docs"/>
  <xsl:template match="text()" mode="op-inner"/>
  <xsl:template match="text()" mode="interface-inner"/>
  <xsl:template match="text()"/>
</xsl:stylesheet>
