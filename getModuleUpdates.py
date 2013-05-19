#! /usr/bin/env python
"""Grabs the tag list from a github project and displays it in an XML format compatible with the Drupal project update system.
"""

from github import Github
import githubOrgConfiguration as configValues
from lxml import etree
from mod_python import apache
from re import search
from urlparse import parse_qsl

__author__ = "Jacob Sanford"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Jacob Sanford"
__email__ = "jsanford@unb.ca"
__status__ = "Production"


def handler(req):
    url_queries= dict(
                      parse_qsl(req.subprocess_env['QUERY_STRING'])
                      )
    repo_id=url_queries['p']
    core_version=url_queries['c']
    projects_to_build=(
                       get_git_tags(
                                    configValues.oauth_token,
                                    req,
                                    configValues.repo_user,
                                    repo_id,
                                    core_version
                                    )
                       )
    if projects_to_build:
        req.content_type = 'text/xml'
        req.write(
                  build_project_xml(
                          sorted(projects_to_build, key=lambda k: k['name'], reverse=True),
                          repo_id,
                          core_version)
                  )
        return apache.OK
    return apache.OK

def get_git_tags(oauth_token,req,repo_user,repo_id,core_version_filter):
    try:
        releases_to_build=[]
        g = Github(oauth_token,user_agent='Drupal Update Github Connector')
        tags=g.get_user(repo_user).get_repo(repo_id).get_tags()
        for cur_tag in tags:
            if core_version_filter in cur_tag.name:
                releases_to_build.append(
                {
                 'name' : cur_tag.name,
                 'commit' : cur_tag.commit.sha,
                 'date' : cur_tag.commit.commit.author.date,
                 'tarball' : cur_tag.tarball_url,
                }
                )
        return releases_to_build
    except:
        req.write('Error communicating with GitHub!')
        return False

def build_project_xml(releases_to_build,project_id,core_version):
    latest_release_string=get_most_recent_tag(releases_to_build)
    default_major_id=get_version_major_int(latest_release_string)

    xml_root = etree.Element('project')
    etree.SubElement(xml_root,'title').text=project_id
    etree.SubElement(xml_root,'short_name').text=project_id
    etree.SubElement(xml_root,'creator').text='UNB Libraries'
    etree.SubElement(xml_root,'api_version').text=core_version
    etree.SubElement(xml_root,'recommended_major').text=default_major_id
    etree.SubElement(xml_root,'supported_majors').text=default_major_id
    etree.SubElement(xml_root,'default_major').text=default_major_id
    etree.SubElement(xml_root,'project_status').text='published'
    etree.SubElement(xml_root,'link').text='http://www.github.com/unb-libraries/' + project_id

    terms_tag=etree.Element('terms')
    xml_root.append(terms_tag)

    cur_term_tag=etree.Element('term');
    etree.SubElement(cur_term_tag,'name').text='Projects'
    etree.SubElement(cur_term_tag,'value').text='Modules'
    terms_tag.append(cur_term_tag)

    cur_term_tag=etree.Element('term');
    etree.SubElement(cur_term_tag,'name').text='Development status'
    etree.SubElement(cur_term_tag,'value').text='Under active development'
    terms_tag.append(cur_term_tag)

    cur_term_tag=etree.Element('term');
    etree.SubElement(cur_term_tag,'name').text='Maintenance status'
    etree.SubElement(cur_term_tag,'value').text='Actively maintained'
    terms_tag.append(cur_term_tag)

    releases_tag=etree.Element('releases')
    xml_root.append(releases_tag)

    for cur_release_dict in releases_to_build :
        cur_release_tag=etree.Element('release');
        etree.SubElement(cur_release_tag,'name').text=project_id + ' ' + cur_release_dict['name']
        etree.SubElement(cur_release_tag,'version').text=cur_release_dict['name']
        etree.SubElement(cur_release_tag,'version_major').text=get_version_major_int(cur_release_dict['name'])
        etree.SubElement(cur_release_tag,'version_extra').text=get_version_extra(cur_release_dict['name'])
        etree.SubElement(cur_release_tag,'status').text='published'
        etree.SubElement(cur_release_tag,'release_link').text='http://www.github.com/unb-libraries/' + project_id
        etree.SubElement(cur_release_tag,'download_link').text=cur_release_dict['tarball']
        etree.SubElement(cur_release_tag,'date').text=cur_release_dict['date'].strftime('%s')
        releases_tag.append(cur_release_tag)

    return etree.tostring(xml_root, pretty_print=True, xml_declaration=True, encoding="utf-8")

def get_most_recent_tag(release_list):
    tag_strings=[]
    skip_list=['dev']
    for cur_release in release_list:
        tag_strings.append(cur_release['name'])
    for sorted_tag in sorted(tag_strings,reverse=True):
        if not any([sorted_tag.find(word) != -1 for word in skip_list]):
            return sorted_tag
    return False

def get_version_major_int(tag_string):
    major_match = search('^[678]\.x-([1-9])\.[0-9x]{1,3}', tag_string)
    if major_match:
        return major_match.group(1)
    return '1'

def get_version_extra(tag_string):
    for cur_extra_string in ['dev'] :
        if cur_extra_string in tag_string :
            return cur_extra_string
    return ''
