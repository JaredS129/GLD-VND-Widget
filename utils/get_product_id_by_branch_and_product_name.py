from classes.ProductTree import ProductTree


def get_product_id_by_branch_and_product_name(product_tree: ProductTree, branch_name: str, product_name: str) -> int:
    for branch in product_tree.branches:
        if branch.name == branch_name:
            for product in branch.products:
                if product.name == product_name:
                    return product.product_id
    return -1