import logging


class CompareDicts:
    """Class with multiple methods for analyzing pre/post check commands already transformed to dicts."""

    def __init__(self, pre_dict, post_dict):
        """
        Constructor
        Args:
            pre_dict:
            post_dict:
        """
        self.pre_dict = pre_dict
        self.post_dict = post_dict

    def _compare_dicts(self, pre: dict, post: dict, missing: list, new: list, changed: list, path='') -> None:
        """Recursively compares two dictionaries and analyze and appends to argument lists found differences.
        Compares keys and values as strings, detects if value is another dict or list and inspects it.

        Args:
            pre: pre-check dictionary
            post: post-check dictionary
            missing: list to append messages about items which were in pre-check but are missing in post-check
            new: list to append messages about new items found in post-check
            changed: list to append messages about differences between pre and post
            path: ignore, not used with first call (used for recursion)

        Returns:
            None as it is recursive method and it adds messages to existing lists.
            It requires wrapper method to collect messages.
        """
        for only_pre in pre.keys() - post.keys():
            missing.append("{} {} not found in post-dict".format(path, only_pre))

        for only_post in post.keys() - pre.keys():
            new.append("{} {} new in post-dict".format(path, only_post))

        path_stack = []
        for key in pre.keys() & post.keys():
            if type(pre[key]) is dict:
                path_stack.append(path)
                if path == "":
                    path = str(key)
                else:
                    path = path + " " + str(key)
                self._compare_dicts(pre[key], post[key], missing, new, changed, path=path)
                path = path_stack.pop()
            elif pre[key] != post[key]:
                if type(pre[key]) is list:
                    in_pre = list(set(pre[key]) - set(post[key]))
                    in_post = list(set(post[key]) - set(pre[key]))
                    changed.append("{} {}: {}->{}".format(path, key, in_pre, in_post))
                else:
                    changed.append("{} {}: {}->{}".format(path, key, pre[key], post[key]))

    def get_results(self) -> dict:
        """Wrapper method for _compare_pre_post() to collect messages from dict comparison.

        Returns:
            results = {
                'missing': missing: list,
                'new': new: list,
                'changed': changed: list,
            }
        """
        missing = []
        new = []
        changed = []
        pre = self.pre_dict
        post = self.post_dict

        if all([pre, post]):  # both dicts are not empty
            self._compare_dicts(pre, post, missing, new, changed)
            results = {'missing': missing, 'new': new, 'changed': changed}
            return results

        elif any([pre, post]):  # one dict is empty
            logging.warning('Unable to analyze. One of input dictionaries is empty.')
            if not pre:
                results = {'missing': ['Unable to analyze. Pre not found.'], 'new': new, 'changed': changed}
            else:
                results = {'missing': ['Unable to analyze. Post not found.'], 'new': new, 'changed': changed}
            return results
        else:
            logging.warning('Nothing to compare')
