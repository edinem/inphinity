from django.urls import path, include, reverse
from rest_framework.urlpatterns import format_suffix_patterns

#from . import views_family
from . import view_login
#from .views import views_family


urlpatterns = [
    path('ppicogscore/', include('inphinity_orm.urls_api_rest.urls_ppiCogScore')),
    path('cogmethodscore/', include('inphinity_orm.urls_api_rest.urls_cogMethodScore')),
    path('coginteractsource/', include('inphinity_orm.urls_api_rest.urls_cogInteractionSource')),
    path('cogsourceinfo/', include('inphinity_orm.urls_api_rest.urls_cogSourceInformation')),
    path('coginteractpair/', include('inphinity_orm.urls_api_rest.urls_cogInteractionPair')),
    path('sourcecog/', include('inphinity_orm.urls_api_rest.urls_sourceCog')),
    path('proteincog/', include('inphinity_orm.urls_api_rest.urls_proteinCog')),
    path('cog/', include('inphinity_orm.urls_api_rest.urls_cog')),
    path('ppipfamscore/', include('inphinity_orm.urls_api_rest.urls_ppiPfamScore')),
    path('ppiinteractsource/', include('inphinity_orm.urls_api_rest.urls_ppiInteractionSource')),
    path('ppi/', include('inphinity_orm.urls_api_rest.urls_ppi')),
    path('ppisource/', include('inphinity_orm.urls_api_rest.urls_ppiSource')),
    path('pfammethodscore/', include('inphinity_orm.urls_api_rest.urls_pfamMethodScore')),
    path('proteinpfam/', include('inphinity_orm.urls_api_rest.urls_proteinPfam')),
    path('sourcepfam/', include('inphinity_orm.urls_api_rest.urls_sourcePfam')),
    path('domaininteractscore/', include('inphinity_orm.urls_api_rest.urls_domainInteractionScore')),
    path('domainmethodscore/', include('inphinity_orm.urls_api_rest.urls_domainMethodScore')),
    path('domaininteractsource/', include('inphinity_orm.urls_api_rest.urls_domainInteractionSource')),
    path('domainsourceinf/', include('inphinity_orm.urls_api_rest.urls_domainSourceInformation')),
    path('domainintpair/', include('inphinity_orm.urls_api_rest.urls_domainInteractionPair')),
    path('domain/', include('inphinity_orm.urls_api_rest.urls_domain')),
    path('couple/', include('inphinity_orm.urls_api_rest.urls_couple')),
    path('lysistype/', include('inphinity_orm.urls_api_rest.urls_lysisType')),
    path('levelinteract/', include('inphinity_orm.urls_api_rest.urls_levelInteraction')),
    path('intervalidity/', include('inphinity_orm.urls_api_rest.urls_interactionValidity')),
    path('protein/', include('inphinity_orm.urls_api_rest.urls_protein')),
    path('wholedna/', include('inphinity_orm.urls_api_rest.urls_wholeDNA')),
    path('contig/', include('inphinity_orm.urls_api_rest.urls_contig')),
    path('gene/', include('inphinity_orm.urls_api_rest.urls_gene')),
    path('bacteriophage/', include('inphinity_orm.urls_api_rest.urls_bacteriophage')),
    path('bacterium/', include('inphinity_orm.urls_api_rest.urls_bacterium')),
    path('baltimoreclass/', include('inphinity_orm.urls_api_rest.urls_baltimoreClassification')),
    path('sourcedata/', include('inphinity_orm.urls_api_rest.urls_sourceData')),
    path('personresp/', include('inphinity_orm.urls_api_rest.urls_personResponsible')),
    path('family/', include('inphinity_orm.urls_api_rest.urls_family')),
    path('genus/', include('inphinity_orm.urls_api_rest.urls_genus')),
    path('specie/', include('inphinity_orm.urls_api_rest.urls_specie')),
    path('strain/', include('inphinity_orm.urls_api_rest.urls_strain')),
    path('login/', view_login.authenticate_user),
]

urlpatterns = format_suffix_patterns(urlpatterns)