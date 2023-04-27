from typing import Callable, List, Optional

from rex.utils.logging import logger

from doctree.data.definition import (
    Action,
    HeadingNode,
    Node,
    NodeType,
    RootNode,
    TextNode,
)
from doctree.utils import guid as G


def move_pointer(past_node: Node, content: list, action: Action):
    """
    move pointer, return the new node.
        if action is reduce, do pointer changing only,
        otherwise merge the content or create new node

    Args:
        past_node: node pointer
        content: list of text content
        action: current predicted action

    Returns:
        curr_node: new node
        left_content: if action is reduce, then return the intact `content`,
            otherwise the left_content is `None`
    """
    left_content = None
    if action in {Action.SubHeading, Action.SubText}:
        curr_node = {Action.SubHeading: HeadingNode, Action.SubText: TextNode}[action]()
        if len(past_node.children) < 1:
            past_node_guid = G.parse_guid(past_node.guid)
            past_node_guid.append(0)
            curr_guid = past_node_guid
        else:
            last_guid = G.parse_guid(past_node.children[-1].guid)
            last_guid[-1] += 1
            curr_guid = last_guid
        curr_guid = G.generate_guid(curr_guid)
        curr_node.guid = curr_guid
        curr_node.children = list()
        curr_node.parent = past_node
        curr_node.content = content
        past_node.children.append(curr_node)
    elif action == Action.Concat:
        past_node.content.extend(content)
        curr_node = past_node
    else:
        # action is Reduce
        curr_node = past_node.parent
        left_content = content
    return curr_node, left_content


def decode_tree(
    predict_api: Callable, input_buffer: List[str], post_process: Optional[bool] = False
) -> Node:
    """
    decode a tree from input texts

    Args:
        predict_api: function that takes `stack_top_content` (`List[str]`)
            and `input_content` (`List[str]`) as inputs
            and predict an `action` (`Action`)
        input_buffer: list of strings for the input
        post_process: whether to use handcraft post process rules

    Returns:
        root node of the tree
    """
    root_node = RootNode(guid="0")
    past_node = root_node
    for input_content in input_buffer:
        left_content = [input_content]
        while left_content is not None:
            action = predict_api(past_node.content, left_content)
            action = handcraft_action_postprocess(past_node, left_content, action)
            if past_node.label == NodeType.Root and action == Action.Reduce:
                logger.warning(
                    f"content {left_content} is predicted as the superior of ROOT, take it as SubText"
                )
                action = Action.SubText
            past_node, left_content = move_pointer(past_node, left_content, action)
    return root_node


def decode_tree_with_constraint(
    action2probs_predict_api: Callable,
    input_buffer: List[str],
    post_process: Optional[bool] = False,
) -> Node:
    """
    decode a tree from input texts

    Args:
        action2probs_predict_api: function that takes `stack_top_content` (`List[str]`)
            and `input_content` (`List[str]`) as inputs
            and predict an `action` (`Action`)
        input_buffer: list of strings for the input
        post_process: whether to use handcraft post process rules

    Returns:
        root node of the tree
    """
    root_node = RootNode(guid="0")
    past_node = root_node
    for input_content in input_buffer:
        left_content = [input_content]
        while left_content is not None:
            action2probs = action2probs_predict_api(past_node.content, left_content)
            action_prob_pairs = sorted(
                action2probs.items(), key=lambda x: x[1], reverse=True
            )
            action = action_prob_pairs[0][0]
            if past_node.label == NodeType.Root and action in [
                Action.Reduce,
                Action.Concat,
            ]:
                for candidate, _ in action_prob_pairs:
                    if candidate not in [Action.Reduce, Action.Concat]:
                        action = candidate
                        break
            elif past_node.label == NodeType.Text and action in [
                Action.SubHeading,
                Action.SubText,
            ]:
                for candidate, _ in action_prob_pairs:
                    if candidate not in [Action.SubHeading, Action.SubText]:
                        action = candidate
                        break
            past_node, left_content = move_pointer(past_node, left_content, action)
    return root_node


def handcraft_action_postprocess(
    past_node: Node, curr_content: List[str], action: Action
) -> Action:
    """
    Handcraft predicted action adjustment

    Args:
        past_node: former node (top of the total stack)
        curr_content: current content
        action: predicted action

    Returns:
        refreshed_action: action after adjustment
    """
    refreshed_action = action

    # texts are not children of text node, concat them
    if past_node.label == NodeType.Text and action == Action.SubText:
        refreshed_action = Action.Concat

    return refreshed_action
