package exp.data;

public interface ExampleDao {

	Example createExample(final ExampleDto exampleDto) throws GeneralDaoErrorException;

	List<Example> getAllExamplesFiltered(final Long testId, final String begin, final String end, final String status) throws GeneralDaoErrorException;

	Void testExample(final ExampleDto exampleDto) throws GeneralDaoErrorException;

}