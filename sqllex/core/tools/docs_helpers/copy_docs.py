def copy_docs(parent_func: callable, sep='\n'):
    """
    Decorator for class methods to copy __doc__ string
    from parent method or any other class method
    """
    def docs_wrapper(func: callable):
        parent_doc = parent_func.__doc__
        func_doc = func.__doc__

        if not func_doc and parent_doc:
            func.__doc__ = parent_doc
        elif not func_doc and not parent_doc:
            func.__doc__ = sep.join((f"\nChild of '{parent_func.__name__}':\n",))
        elif func_doc and parent_doc:
            func.__doc__ = sep.join((func_doc, f"\nChild of '{parent_func.__name__}':\n", parent_doc))
        else:
            pass
        return func
    return docs_wrapper


__all__ = [
    'copy_docs'
]
