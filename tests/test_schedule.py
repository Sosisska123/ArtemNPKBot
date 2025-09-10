import unittest
from unittest.mock import AsyncMock, Mock, patch
import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from models.schedule import Schedule
from db.database import Database


class TestScheduleDatabase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Create a mock session
        self.mock_session = AsyncMock(spec=AsyncSession)
        self.db = Database(self.mock_session)
        
        # Create test data
        self.test_date = datetime.date(2025, 9, 1)
        self.test_group = "нпк"
        self.test_url = "https://example.com/schedule.pdf"
        
    async def test_save_schedule(self):
        # Setup
        mock_schedule = Schedule(
            id=1,
            group=self.test_group,
            url=self.test_url,
            date=self.test_date,
            schedule_type="regular"
        )
        
        self.mock_session.add = Mock()
        self.mock_session.commit = AsyncMock()
        self.mock_session.refresh = AsyncMock()
        self.mock_session.in_transaction = Mock(return_value=False)  # Not in transaction
        
        # Execute
        result = await self.db.save_schedule(
            self.test_group, 
            self.test_date, 
            self.test_url, 
            "regular"
        )
        
        # Verify
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_awaited_once()
        self.mock_session.refresh.assert_awaited_once()
        
    async def test_save_schedule_in_transaction(self):
        # Setup
        mock_schedule = Schedule(
            id=1,
            group=self.test_group,
            url=self.test_url,
            date=self.test_date,
            schedule_type="regular"
        )
        
        self.mock_session.add = Mock()
        self.mock_session.commit = AsyncMock()
        self.mock_session.refresh = AsyncMock()
        self.mock_session.flush = AsyncMock()
        self.mock_session.in_transaction = Mock(return_value=True)  # In transaction
        
        # Execute
        result = await self.db.save_schedule(
            self.test_group, 
            self.test_date, 
            self.test_url, 
            "regular"
        )
        
        # Verify
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_not_awaited()
        self.mock_session.refresh.assert_not_awaited()
        self.mock_session.flush.assert_awaited_once()
        
    async def test_get_schedule_modified_priority(self):
        # Setup - return modified schedule first
        mock_modified = Schedule(
            id=1,
            group=self.test_group,
            url=self.test_url,
            date=self.test_date,
            schedule_type="modified"
        )
        
        # Mock the session execute method
        mock_result = Mock()
        mock_result.scalar_one_or_none = Mock(side_effect=[mock_modified, None])  # First call returns modified, second returns None
        self.mock_session.execute = AsyncMock(return_value=mock_result)
        
        # Execute
        result = await self.db.get_schedule(self.test_group, self.test_date)
        
        # Verify
        self.assertEqual(result, mock_modified)
        self.assertEqual(result.schedule_type, "modified")
        self.mock_session.execute.assert_awaited()
        
    async def test_get_schedule_fallback_to_regular(self):
        # Setup - no modified schedule, but regular exists
        mock_regular = Schedule(
            id=2,
            group=self.test_group,
            url=self.test_url,
            date=self.test_date,
            schedule_type="regular"
        )
        
        # Mock the session execute method
        mock_result = Mock()
        mock_result.scalar_one_or_none = Mock(side_effect=[None, mock_regular])  # First call returns None, second returns regular
        self.mock_session.execute = AsyncMock(return_value=mock_result)
        
        # Execute
        result = await self.db.get_schedule(self.test_group, self.test_date)
        
        # Verify
        self.assertEqual(result, mock_regular)
        self.assertEqual(result.schedule_type, "regular")
        self.mock_session.execute.assert_awaited()
        
    async def test_get_schedule_none_found(self):
        # Setup - no schedules found
        mock_result = Mock()
        mock_result.scalar_one_or_none = Mock(return_value=None)
        self.mock_session.execute = AsyncMock(return_value=mock_result)
        
        # Execute
        result = await self.db.get_schedule(self.test_group, self.test_date)
        
        # Verify
        self.assertIsNone(result)
        self.mock_session.execute.assert_awaited()
        
    async def test_update_tomorrow_schedule(self):
        # Setup
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        mock_schedule = Schedule(
            id=3,
            group=self.test_group,
            url=self.test_url,
            date=tomorrow,
            schedule_type="modified"
        )
        
        with patch.object(self.db, 'save_schedule', return_value=mock_schedule) as mock_save:
            # Execute
            result = await self.db.update_tomorrow_schedule(self.test_group, self.test_url)
            
            # Verify
            mock_save.assert_awaited_once_with(
                self.test_group,
                tomorrow,
                self.test_url,
                "modified"
            )
            self.assertEqual(result, mock_schedule)


if __name__ == '__main__':
    unittest.main()