from django.test import TestCase
from lists.models import Item, List
       
class ListAndItemModelTest(TestCase):
    
    def save_item(self, item_text, list):
        item = Item()
        item.text = item_text
        item.list = list
        item.save()        
        
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        
        self.save_item('The first (ever) list item', list_)
        self.save_item('Item the second', list_)
        
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)
