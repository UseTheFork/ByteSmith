from byte.domain.agent.schemas import ConstraintSchema


def replace_list(left: list | None, right: list) -> list:
	"""Reducer that replaces the entire list with new values.

	Unlike the default add_messages which appends, this replaces the full list.
	Used with Annotated to handle state updates that should completely replace
	rather than accumulate values.

	Usage: `errors: Annotated[list[AnyMessage], replace_list]`
	"""
	return right


def add_constraints(left: list[ConstraintSchema] | None, right: list[ConstraintSchema]) -> list[ConstraintSchema]:
	"""Reducer that accumulates user-defined constraints for the current invocation.

	Constraints are suggestions or actions the agent should avoid or follow based on
	user feedback (e.g., declined tool calls, rejected edits).

	Usage: `constraints: Annotated[list[ConstraintSchema], add_constraints]`
	"""
	if left is None:
		return right
	return left + right
