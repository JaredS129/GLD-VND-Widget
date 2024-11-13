from classes.ProductTree import ProductTree, Product, Branch
from classes.PriceApi import AllCurrentGoldPricesResponse


def build_product_tree(current_gold_prices: AllCurrentGoldPricesResponse) -> ProductTree:
    product_tree: ProductTree = ProductTree()
    for gold_price_data in current_gold_prices.data:
        branch_exists = False
        for branch in product_tree.branches:
            if branch.name == gold_price_data.branch_name:
                branch_exists = True
                product_exists = False
                for product in branch.products:
                    if product.name == gold_price_data.type_name:
                        product_exists = True
                        break
                if not product_exists:
                    product = Product(name=gold_price_data.type_name, product_id=gold_price_data.price_data_id)
                    branch.products.append(product)
                break
        if not branch_exists:
            branch = Branch(name=gold_price_data.branch_name, products=[
                Product(name=gold_price_data.type_name, product_id=gold_price_data.price_data_id)])
            product_tree.branches.append(branch)
    return product_tree