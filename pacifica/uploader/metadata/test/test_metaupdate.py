#!/usr/bin/python
"""Module used to test the MetaUpdate module."""
from unittest import TestCase
from pacifica.uploader.metadata.MetaUpdate import MetaUpdate
from pacifica.uploader.metadata.MetaData import MetaObj


class TestMetaUpdate(TestCase):
    """Test the MetaUpdate class."""

    def test_update_parents(self):
        """Test the MetaUpdate update_parents method."""
        md_update = MetaUpdate('dmlb2001')
        md_update.append(
            MetaObj(
                destinationTable='Transactions.submitter',
                diplayFormat='%(first_name)s %(last_name)s',
                displayTitle='Currently Logged On',
                displayType='logged_on',
                metaID='logon',
                queryDependency={'network_id': 'logon'},
                queryFields=['first_name', 'last_name', '_id'],
                sourceTable='users',
                value='dmlb2001',
                valueField='_id'
            )
        )
        md_update.append(
            MetaObj(
                destinationTable='Transactions.instrument',
                diplayFormat='%(_id)s %(name_short)s - %(display_name)s',
                displayTitle='Instrument',
                displayType='select',
                metaID='instrumentByID',
                queryDependency={'_id': 'instrumentByID'},
                queryFields=['display_name', 'name_short', '_id'],
                sourceTable='instruments',
                value=54,
                valueField='_id'
            )
        )
        md_update.append(
            MetaObj(
                destinationTable='Transactions.proposal',
                diplayFormat='%(_id)s %(title)s',
                displayTitle='Proposal',
                displayType='select',
                metaID='ProposalByInstrument',
                queryDependency={'instrument_id': 'instrumentByID'},
                queryFields=['title', '_id'],
                sourceTable='proposals',
                value=None,
                valueField='_id'
            )
        )
        md_update.append(
            MetaObj(
                diplayFormat='Proposal %(_id)s',
                directoryOrder=0,
                displayType='directoryTree',
                metaID='ProposalDirectory',
                queryDependency={'_id': 'ProposalByInstrument'},
                queryFields=['_id'],
                sourceTable='proposals',
                value=None,
                valueField='_id'
            )
        )
        md_update.update_parents('ProposalDirectory')
        self.assertTrue(md_update['ProposalByInstrument'].value)
        self.assertEqual(md_update['ProposalDirectory'].value, u'1234a')
        self.assertTrue(md_update.is_valid())