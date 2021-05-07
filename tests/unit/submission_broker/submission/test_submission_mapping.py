import unittest
from submission_broker.submission.submission import Submission, HandleCollision


class TestSubmissionMapping(unittest.TestCase):
    def setUp(self) -> None:
        self.entity_type = 'test'
        self.index = 'index'
        self.collision_type = [
            HandleCollision.UPDATE,
            HandleCollision.OVERWRITE,
            HandleCollision.IGNORE
        ]

    def test_mapping_identical_index_should_return_same_entity(self):
        for collision in self.collision_type:
            with self.subTest(collision=collision):
                submission = Submission(collision)
                entity1 = submission.map(self.entity_type, self.index, {})
                entity2 = submission.map(self.entity_type, self.index, {})
                self.assertEqual(entity1, entity2)

    def test_mapping_identical_index_should_error(self):
        submission = Submission(HandleCollision.ERROR)
        submission.map(self.entity_type, self.index, {})
        with self.assertRaises(IndexError):
            submission.map(self.entity_type, self.index, {})

    def test_mapping_identical_index_should_ignore_entity_attributes(self):
        submission = Submission(HandleCollision.IGNORE)
        attributes1 = {'first_key': 'kept'}
        attributes2 = {'second_key': 'ignored'}
        entity = submission.map(self.entity_type, self.index, attributes1)
        submission.map(self.entity_type, self.index, attributes2)
        self.assertEqual(attributes1, entity.attributes)

    def test_mapping_identical_index_should_overwrite_entity_attributes(self):
        submission = Submission(HandleCollision.OVERWRITE)
        attributes1 = {'first_key': 'forgotten'}
        attributes2 = {'second_key': 'overwritten'}
        entity = submission.map(self.entity_type, self.index, attributes1)
        submission.map(self.entity_type, self.index, attributes2)
        self.assertEqual(attributes2, entity.attributes)

    def test_mapping_identical_index_should_update_entity_attributes(self):
        submission = Submission(HandleCollision.UPDATE)
        attributes1 = {
            'initial': 'first',
            'both': 'first'
        }
        attributes2 = {
            'second': 'new',
            'both': 'new'
        }
        expected_attributes = {
            'initial': 'first',
            'second': 'new',
            'both': 'new'
        }
        entity = submission.map(self.entity_type, self.index, attributes1)
        submission.map(self.entity_type, self.index, attributes2)
        self.assertDictEqual(expected_attributes, entity.attributes)

    def test_has_data_should_start_false(self):
        submission = Submission()
        self.assertFalse(submission.has_data())

    def test_has_data_should_become_true(self):
        submission = Submission()
        submission.map(self.entity_type, self.index, {})
        self.assertTrue(submission.has_data())
